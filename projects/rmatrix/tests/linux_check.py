import os,pty,fcntl,termios,struct,subprocess,select,time,sys,tempfile,codecs,atexit
from pathlib import Path
import pyte
BINARY=str(Path(sys.argv[1]).resolve())
SESSIONS=[]
@atexit.register
def cleanup():
    for session in SESSIONS:
        if session.p.poll() is None: session.p.terminate();session.p.wait(timeout=2)

MODES=['rain','waterfall','waves','spiral','glitch','starfield','blackhole','galaxy','aurora','plasma','tunnel','fireworks']
class Session:
    def __init__(self,mode='rain',width=160,height=61,name=False):
        self.master,slave=pty.openpty();self.width=width;self.height=height
        fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',height,width,0,0))
        self.screen=pyte.Screen(width,height);self.stream=pyte.Stream(self.screen)
        self.config=tempfile.TemporaryDirectory();env=dict(os.environ,TERM='xterm-256color',XDG_CONFIG_HOME=self.config.name)
        args=[BINARY,'--mode',mode,'--seed','42','--fps','60',*(['--name','AI'] if name else ['--no-name'])]
        self.p=subprocess.Popen(args,stdin=slave,stdout=slave,stderr=slave,env=env)
        os.close(slave);self.decoder=codecs.getincrementaldecoder("utf-8")();self.raw=bytearray();SESSIONS.append(self);self.read(.25)
    def read(self,seconds):
        until=time.monotonic()+seconds;out=bytearray()
        while time.monotonic()<until:
            if select.select([self.master],[],[],min(.025,max(0,until-time.monotonic())))[0]:
                try:data=os.read(self.master,262144)
                except OSError:break
                out.extend(data);self.raw.extend(data);self.stream.feed(self.decoder.decode(data))
        assert b'runtime error' not in self.raw.lower(), self.raw[-2000:]
        assert self.p.poll() is None, (self.p.returncode,self.raw[-2000:])
        return out
    def key(self,keys):os.write(self.master,keys);return self.read(.15)
    def until(self,predicate,label):
        deadline=time.monotonic()+2
        while not predicate():
            assert time.monotonic()<deadline, label
            self.read(.025)
    def snapshot(self):return [[self.screen.buffer[y][x] for x in range(self.width)] for y in range(self.height)]
    def resize(self,width,height):
        fcntl.ioctl(self.master,termios.TIOCSWINSZ,struct.pack('HHHH',height,width,0,0))
        self.width,self.height=width,height;self.screen.resize(lines=height,columns=width)
        self.read(.25)
    def close(self,key=b'q',code=0):
        start=time.monotonic();os.write(self.master,key)
        while self.p.poll() is None and time.monotonic()-start<2:
            if select.select([self.master],[],[],.02)[0]:
                try:os.read(self.master,262144)
                except OSError:break
        self.p.wait(timeout=2);assert self.p.returncode==code,self.p.returncode
        assert time.monotonic()-start<.5,'Quit too slow'
        os.close(self.master);self.config.cleanup()
for mode in MODES:
    s=Session(mode);assert mode.upper() in '\n'.join(s.screen.display).upper(),mode
    s.key(b'epsc');s.key(b'[]+-');s.close()
print('12 scenes, effects, palettes, density and speed controls execute and quit cleanly')
s=Session(name=True);s.key(b' ')
assert 'PAUSED' in s.screen.display[-1]
assert len(s.read(.3))==0,'Paused app still writes'
snapshot=s.snapshot();s.key(b'?');assert 'RMATRIX / CONTROLS' in '\n'.join(s.screen.display)
s.key(b'?');assert s.snapshot()==snapshot,'Closing help did not restore scene/styles'
s.key(b'\t');assert 'RMATRIX / SCENES' in '\n'.join(s.screen.display)
s.key(b'\t');assert s.snapshot()==snapshot,'Closing picker did not restore scene/styles'
s.key(b'n');s.key(b'n');assert s.snapshot()==snapshot,'Name overlay toggle left ghost cells'
s.resize(10,4);s.until(lambda:'Resize' in '\n'.join(s.screen.display),'tiny-terminal redraw')
assert len(s.read(.3))==0,'Small terminal still redraws'
s.resize(80,24);s.until(lambda:'PAUSED' in s.screen.display[-1],'paused HUD after resize')
assert len(s.read(.3))==0,'Resize did not settle while paused'
s.key(b'h');s.key(b'h');assert 'PAUSED' in s.screen.display[-1]
s.key(b' ');assert len(s.read(.15))>0,'Resume failed'
s.close()
s=Session();s.close(b'\x03',130)
print('Pause silence, help/picker/name restoration, tiny-window resize, HUD, resume and Ctrl+C passed')
