# Ramos examples

Small, runnable native Ramos programs for **Ramos 0.25.0 preview**, on Linux x64 and
Windows x64. Part of the [Ramos project hub](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/ecosystem.md).
All runtime code is Ramos; Python is optional setup and test tooling.

## Start here

Clone this repository, then download `ramos-linux-x86_64` or `ramos.exe` from the
[0.25.0 preview](https://github.com/zackmsa777-a11y/ramos/releases/tag/v0.25.0).
On Linux rename the download to `ramos` and run `chmod +x ramos`.
Alternatively, Python 3 installs the pinned binary with a SHA-256 check:

```sh
python tools/compiler.py
```

Linux:

```sh
./ramos run examples/hello.ramos
./ramos build examples/rgrep.ramos -o build/rgrep
./build/rgrep weave examples/library_demo.ramos
./ramos run examples/gui_hello.ramos --gui
```

Create `build/` first (`mkdir -p build`). GUI programs require GTK3 and a display
on Linux; on Ubuntu install `libgtk-3-0`.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force build
.\ramos.exe run examples/hello.ramos
.\ramos.exe build examples/rgrep.ramos -o build/rgrep.exe
.\build\rgrep.exe weave examples/library_demo.ramos
.\ramos.exe run examples/gui_hello.ramos --gui
```

## Choose an example

| Area | Sources in `examples/` | What they show |
| --- | --- | --- |
| First programs | `hello`, `calculator`, `control_flow`, `functions` | Syntax, checked arithmetic and functions |
| Data and syntax | `buffers`, `library_demo`, `usability`, `easier_syntax` | Bytes, libraries, strings, structs, arrays and ranges |
| Stdin and text | `input`, `line_stats`, `rnumber`, `rstats` | Unicode lines, streaming text and decimal input |
| Files and OS | `rcopy`, `rgrep`, `rfind`, `rrun` | Exclusive copy, literal search, directory traversal and child processes |
| Terminal UI | `rview` | Full-screen file viewer with keyboard navigation |
| Desktop GUI | `gui_hello`, `notes` | Native controls, resize layout and file pickers; build with `--gui` |
| Numerical output | `mandelbrot` | Float64 rendering to an image file |

Every source has a `.ramos` extension. Read its usage checks before running file
or OS tools. `rcopy` and Notes refuse to overwrite existing files. `rview` needs
an interactive terminal. The small arithmetic `calculator` example is distinct
from the larger [scientific calculator](https://github.com/zackmsa777-a11y/ramos-calculator).

## Larger terminal project

[rmatrix](projects/rmatrix/README.md) adds twelve animations with changed-cell
rendering, elapsed-time frame pacing, overlays and keyboard controls. Its source
is Ramos; its Python terminal model is a test tool. See its measured app-specific
[performance](projects/rmatrix/PERFORMANCE.md).

## Check and contribute

```sh
python -m pip install -r requirements-test.txt
python tools/check.py
```

This verifies pinned source hashes, compiles all 20 programs for both native
targets and runs CLI acceptance checks on the current OS. CI runs on Linux and
Windows. Interactive TUI/GUI behavior is not implied by compilation alone;
upstream release evidence documents those platform tests.

These examples and `stdlib/` originate at the source commit in
[upstream.json](upstream.json). Standard-library files are a pinned snapshot,
not a second implementation. Develop new examples here; fixes to the compiler
or standard library belong in [ramos](https://github.com/zackmsa777-a11y/ramos).
Existing compiler release/test snapshots remain available there for compatibility.

Read the [HTML book](https://zackmsa777-a11y.github.io/ramos-docs/) or
[Markdown agent guide](https://github.com/zackmsa777-a11y/ramos-docs/blob/main/book/16-agent-guide.md).
Find the five repositories through the hub and the shared `ramos` topic.

## Ramos family

[Source](https://github.com/zackmsa777-a11y/ramos) ·
[Book](https://github.com/zackmsa777-a11y/ramos-docs) ·
[Examples](https://github.com/zackmsa777-a11y/ramos-examples) ·
[Calculator](https://github.com/zackmsa777-a11y/ramos-calculator) ·
[Benchmarks](https://github.com/zackmsa777-a11y/ramos-benchmarks)

Browse the shared [Ramos topic](https://github.com/topics/ramos).

## Native integer sorting

`rsort` uses the 0.21 list capacity/status and constant-storage sorting helpers:

```sh
./ramos build examples/rsort.ramos -o build/rsort
printf '3\n-4\n3\n0\n' | ./build/rsort
./build/rsort numbers.txt
```

It accepts one signed int64 per line from stdin or a streamed file, keeps
duplicates, and rejects malformed input or more than 131072 numbers with a line
number and exit 2. The input is read/validated before output begins.
See [collection ownership and limits](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/collections.md).

The `deep_recursion.ramos` example preserves pending values through 501 recursive
frames and prints `125250`. The compiler now checks both a 1,024-call limit
and a 4 MiB stack budget; see the [stack policy](https://github.com/zackmsa777-a11y/ramos/blob/main/docs/stack-budget.md).

## Native drawing example

`examples/plot.ramos` uses the new `stdlib/draw.ramos` library for a native
interactive curve: change the curve with its button and redraw on resize.
Build with `./ramos build examples/plot.ramos -o build/plot --gui`, or
`.\ramos.exe build examples/plot.ramos -o build/plot.exe --gui` on Windows.
The compiler source repository verifies the actual plot on both desktops.

`examples/math_output.ramos` demonstrates exact scientific and compact numerical
output, including tiny nonzero values and ties-to-even rounding.

The new `examples/scaling.ramos` opens a logical-coordinate window and logs
actual DPI events. Follow the [Windows display test](https://github.com/zackmsa777-a11y/ramos/blob/v0.25.0/docs/gui-scaling.md).
Initial Windows native checks and genuine GTK scale changes pass; genuine
Windows display changes remain pending. The other examples keep their existing
opening policy. No new speed claim.
