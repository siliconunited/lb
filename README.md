# Little Benchmark
> A framework for benchmarking microchips.

> Please help keep the project alive by donating.
<a href="https://liberapay.com/robksawyer/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg"></a>

## Options for benchmarking

### Mother Device w/Microchip
- This software could run on a mother device e.g. Raspberry Pi. `lb` would then have a benchmark written (by you or maybe you get lucky and find one) for a specific chip under test (CUT) or a device under test (DUT).
- **Note:** The benchmark written should be placed in the `platform/benchmarks` folder and follow the benchmark creation rules (need to be written – see examples in the `python/benchmarks` folder for now).

### Benchmarking Single Board Computer
- Right now the software is written in Python, so as long as the device is running Linux and has Python installed, you could fire benchmarks off using `lb run MyBenchmark`.

![alpha](https://s10.postimg.org/r7o2cguq1/lb_image.png)

# Goal

- Build a framework that makes microchip and Single Board Computer (SBC) benchmarking easier.
- Benchmark agnostic
- Support as many devices and platforms as possible.

# Inspiration
- [Phoronix Test Suite](http://www.phoronix-test-suite.com/) (PTS) for PC benchmarking
- This [Sparkfun article](https://learn.sparkfun.com/tutorials/single-board-computer-benchmarks). Although, work had already started on `lb` prior to the article.

# Engineer? Here to help code? Have a look at the following.

## Platforms
- Python Version: [README](python/README.md)
- Arduino Version: [README](arduino/README.md)
