from pathlib import Path
import os,subprocess,sys,platform
import pyte
PROJECT=Path(__file__).resolve().parents[1]
ROOT=PROJECT.parents[1]
root=ROOT/'build/rmatrix-check';root.mkdir(parents=True,exist_ok=True)
compiler=Path(sys.argv[1]).resolve()
marker=b'\x1b]777;fixture\x07'
outputs={}
for version,renderer in [('baseline',PROJECT/'tests/reference/render_full.ramos'),('candidate',PROJECT/'render.ramos')]:
    prefix=os.path.relpath(renderer,root).replace(os.sep,'/')
    source=f'weave "{prefix}"\n' 
    source+='''fn main() {
let marker = bytes_copy("X]777;fixtureX")
buffer_set(marker, 0, 27)
buffer_set(marker, buffer_len(marker)-1, 7)
let grid = Grid(80, 23, array(int64,1840,0), array(int64,1840,0), array(int64,1840,0), array(int64,256,0))
let cfg = Cfg(0,0,0,70,100,60,42)
let ui = UI(false,false,false,true,false,false,false,false,false,true,0,0)
let hist = Hist(array(int64,1840,0), array(int64,1840,0), array(int64,1840,0))
let lut = Lut(array(int64,256,0), array(int64,65,0))
lut_build(lut)
let out = Row(buffer(131072),0)
'''
    if version=='candidate': source+='let painted = Paint(array(int64,1840,0), array(int64,1840,0), false, s"")\n'
    source+='''for step in 0..40 {
    let frame = step / 2
    cfg.pal = frame % 8
    ui.echo = frame % 3 == 1
    ui.pulse = frame % 3 == 2
    ui.scan = frame % 2 == 1
    for i in 0..1840 {
        grid.g[i] = 33 + (i * 11 + frame) % 90
        grid.l[i] = (i * 17 + frame * 47) % 1001
        grid.u[i] = (i * 23 + frame * 71) % 1000
    }
    row_reset(out)
'''
    source+='    emit_grid(grid,cfg,ui,hist,out,lut,0,frame*11'+(',painted' if version=='candidate' else '')+')\n'
    source+='    hud_draw(80,24,cfg,ui'+(',painted' if version=='candidate' else '')+')\n'
    source+='    stdout(marker)\n}\n}\n'
    path=root/(version+'-render.ramos');path.write_text(source)
    binary=root/(version+'-render'+('.exe' if platform.system()=='Windows' else ''))
    subprocess.run([str(compiler),'build',str(path),'-o',str(binary),'--force'],check=True)
    result=subprocess.run([str(binary)],capture_output=True,timeout=10)
    assert result.returncode==0,result.stderr
    frames=result.stdout.split(marker)
    assert len(frames)==41,len(frames)
    screen=pyte.Screen(80,24);stream=pyte.Stream(screen)
    snapshots=[]
    for data in frames[:-1]:
        stream.feed(data.decode('ascii'))
        snapshots.append([[screen.buffer[y][x] for x in range(80)] for y in range(24)])
    outputs[version]=snapshots
for f,(a,b) in enumerate(zip(outputs['baseline'],outputs['candidate'])):
    if a != b:
        found=0
        for y in range(24):
            for x in range(80):
                if a[y][x]!=b[y][x] and found < 8:
                    print('Mismatch',f,y,x,a[y][x],b[y][x]);found+=1
        raise AssertionError('Screen/style mismatch in diff renderer')
print('40 reference screen/style frames match across all palettes, echo, pulse and scanlines')
