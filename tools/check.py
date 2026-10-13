"""Build every example for both targets; exercise portable CLI behavior."""
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from compiler import install
from provenance import check_sources
ROOT = Path(__file__).resolve().parents[1]
check_sources(ROOT)
compiler = install()
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)
windows = platform.system() == "Windows"
for source in sorted((ROOT / "examples").glob("*.ramos")):
    gui = source.stem in ("notes", "gui_hello", "plot")
    for target, suffix in [("linux", ""), ("windows", ".exe")]:
        cmd = [str(compiler), "build", str(source), "-o", str(BUILD / (source.stem + suffix)),
               "--target", target, "--force"]
        if gui: cmd.append("--gui")
        subprocess.run(cmd, check=True, cwd=ROOT)
suffix = ".exe" if windows else ""
def run(name, *args, data=b"", code=0):
    p = subprocess.run([str(BUILD / (name + suffix)), *map(str,args)], input=data,
                       capture_output=True, timeout=30)
    assert p.returncode == code, (name,p.returncode,p.stderr)
    return p.stdout.replace(b"\r\n", b"\n")
assert run("hello") == b"Hello, Ramos!\n"
assert run("math_output") == b"1.00000e-100\n1e-100\n3.5\n2e+0\n4e+0\n1e+4\n4.9406564584124654e-324\n"
assert run("deep_recursion") == b"125250\n"
assert run("rsort", data=b"3\n-4\n3\n0\n") == b"-4\n0\n3\n3\n"
assert run("rsort", data=b"") == b""
assert run("rsort", data=b"1\nbad\n", code=2) == b""
assert run("line_stats", data="hello\n🌍\n".encode()) == "1: hello\n2: 🌍\nlines=2 characters=6 longest=5\n".encode()
assert run("rstats", data=b"1\n2\n3\n") == b"count=3\nmin=1.000000\nmax=3.000000\nsum=6.000000\nmean=2.000000\n"
run("rstats", data=b"invalid\n", code=2)
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    source, dest = root/"source.txt", root/"copy.txt"
    source.write_bytes("one\nneedle 🌍\nlast\n".encode())
    numbers = root/"numbers é.txt"
    numbers.write_bytes(b"9223372036854775807\r\n-9223372036854775808\r\n0")
    assert run("rsort", numbers) == b"-9223372036854775808\n0\n9223372036854775807\n"
    assert run("rnumber", source) == "1: one\n2: needle 🌍\n3: last\n".encode()
    assert run("rgrep", "needle", source).endswith(":2:needle 🌍\n".encode())
    run("rgrep", "missing", source, code=1)
    run("rcopy", source, dest)
    assert dest.read_bytes() == source.read_bytes()
    run("rcopy", source, dest, code=1)
    assert dest.read_bytes() == source.read_bytes()
print("48 example target builds and 16 CLI acceptance checks passed")

project = ROOT / "projects/rmatrix"
for target, ending in [("linux", ""), ("windows", ".exe")]:
    subprocess.run([str(compiler), "build", str(project / "rmatrix.ramos"),
                    "-o", str(BUILD / ("rmatrix" + ending)), "--target", target,
                    "--force"], check=True, cwd=ROOT)
assert run("rmatrix", "--version").startswith(b"rmatrix 0.2.0")
assert b"plasma" in run("rmatrix", "--help")
run("rmatrix", "--not-a-flag", code=2)
subprocess.run([sys.executable, str(project / "tests/render_check.py"),
                str(compiler)], check=True, cwd=ROOT)
if not windows:
    subprocess.run([sys.executable, str(project / "tests/linux_check.py"),
                    str(BUILD / "rmatrix")], check=True, cwd=ROOT)
print("rmatrix: both targets, CLI behavior and reference renderer checks passed")
