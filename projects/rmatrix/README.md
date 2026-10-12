# rmatrix — native Ramos terminal animations

Twelve terminal scenes, based on [Rust nmatrix](https://github.com/zackmsa777-a11y/nmatrix),
with the scene logic and renderer written in Ramos. Requires **Ramos 0.20.0**
for the native `monotonic_ms()` clock. See [origin.json](origin.json) and the
retained [nmatrix MIT notice](LICENSE.nmatrix).

## Build and run

From the `ramos-examples` repository root, install its pinned compiler with
`python tools/compiler.py`, or download the 0.20.0 release manually:

```sh
mkdir -p build
./ramos build projects/rmatrix/rmatrix.ramos -o build/rmatrix
./build/rmatrix --no-name
./build/rmatrix --mode plasma --palette violet --fps 60 --no-name
./build/rmatrix --demo --palette rainbow
```

An ANSI-compatible interactive terminal is required. Without `--no-name`, the
app prompts for or loads a name and writes its best-effort Linux config under
`$XDG_CONFIG_HOME/rmatrix/config` or `~/.config/rmatrix/config`. Names are ASCII,
1–20 characters. `--no-name` avoids the prompt, banner and config I/O.

Windows PowerShell build:

```powershell
New-Item -ItemType Directory -Force build
.\ramos.exe build projects/rmatrix/rmatrix.ramos -o build/rmatrix.exe
.\build\rmatrix.exe --no-name
```

Linux terminal interaction is verified. Windows uses Ramos's native VT console
support; compiler, clock and noninteractive app checks run natively in Windows CI.
The app is cross-compiled and its noninteractive behavior and renderer run in
Windows CI. Interactive rmatrix controls have not yet been verified on a real
Windows terminal; use Windows Terminal and `--no-name`.

## What changed

- Cache the last displayed glyph/style; emit only changed runs.
- Use a native monotonic clock for deadlines and actual animation time, carrying
  fractional milliseconds for 60 FPS rather than rounding every delay to 16 ms.
- Include rendering/output time in the frame budget; retain input during waits.
- Stop redraws while paused or while a static help/picker view is unchanged.
- Cache the HUD, invalidate covered cells on overlay changes and resize, and
  restore the full scene after leaving a tiny window.
- Emit explicit ANSI intensity resets so bold/faint do not leak between runs.
- Write grid bytes directly, avoiding the bytes → string → bytes round trip.

The [measurement report](PERFORMANCE.md) distinguishes real fast-reader samples
from simulated output backpressure. Improvements are specific to this app and
these workloads, not a language-wide C/Rust speed claim. A sufficiently slow
terminal or remote connection can still limit FPS.

## Scenes, controls and limits

Scenes: rain, waterfall, waves, spiral, glitch, starfield, blackhole, galaxy,
aurora, plasma, tunnel and fireworks. Palettes: emerald, cyan, violet, amber,
rainbow, rose, ice and sunset. Glyph sets: matrix, binary and hex.

Tab picker · `1-9`/`0` scenes · arrows/`m` cycle · `c` colors · `g` glyphs ·
`e`/`p`/`s` effects · `r` surprise · `n` banner · `[`/`]` density ·
`+`/`-` speed · Space pause · `d` demo · `h` HUD · `?` help · `q`/Esc/Ctrl+C quit.
Run `--help` for flags. Default/maximum requested FPS is 60; minimum is 1.

The render grid is capped at 160×60 cells. Basic ANSI colors and fixed-point
approximations remain; truecolor, RGB cross-fades and Rust nmatrix's larger
viewport are not implemented. The clock and rendering changes preserve Ramos's
checked arithmetic, bounds, managed memory and terminal cleanup.

## Check

From the repository root:

```sh
python -m pip install -r requirements-test.txt
python tools/check.py
```

Checks build both targets, compare 40 reference screen/style frames across all
palettes/effects, and exercise actual terminal controls. Python/pyte are test
and setup tools only; compiled animation code runs natively in Ramos.
