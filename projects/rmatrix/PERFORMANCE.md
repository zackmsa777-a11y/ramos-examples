# rmatrix performance evidence

The [full measurement report, raw results, before/after sources and reproduction harness](https://github.com/zackmsa777-a11y/ramos-benchmarks/tree/main/benchmarks/0.20.0/rmatrix)
are maintained in Ramos's benchmark repository.

In one Linux PTY sample with a fast reader, a 160×60 plasma grid, seed 42 and
a 60 FPS target, observed throughput changed from 48.32 to 59.85 FPS and output
from 2.458 to 0.251 MiB/s (about 90% fewer bytes). Three other sampled scenes
also approached 60 FPS. The PTY consumer does not draw pixels, samples are short
and reader buffering affects delivery timestamps. Real-terminal FPS varies.

This is an app-specific result from changed-cell output and proper frame
deadlines. It does not establish an overall language speed score or a Windows
performance claim. See the report for simulated backpressure and pause caveats.
