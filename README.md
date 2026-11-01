# uniLoader for Samsung Galaxy S2 GT-I9100

ARMv7 loader for the international Exynos4210 Galaxy S2. It embeds XNU,
generates Apple boot arguments/device tree, and transfers control from Samsung's
kernel boot path. Companion XNU snapshot: **MALI33, 2026-11-01**.

Published branch: [kernel86-64/uniloader, i9100](https://github.com/kernel86-64/uniloader/tree/i9100).
Companion kernel: [kernel86-64/xnu-i9100, i9100-source](https://github.com/kernel86-64/xnu-i9100/tree/i9100-source).

Based on [kOtusin/uniLoader](https://github.com/kOtusin/uniloader) and
[ivoszbg/uniLoader](https://github.com/ivoszbg/uniLoader). Original GPLv2
[license](LICENSE), [provenance](PROVENANCE.json), [source manifest](SOURCE_MANIFEST.json)
and [upstream README](Documentation/README.upstream.md) are retained.

## One-command build

Use macOS, Apple Command Line Tools with classic ld64, Python 3, make and
`arm-none-eabi-gcc`/binutils. Verified development versions: Apple clang 21.0.0
and GCC 16.2.0. Linux paths are inherited and unverified. Clone the sources into
sibling directories, then build from `uniloader`:

```sh
git clone --branch i9100-source https://github.com/kernel86-64/xnu-i9100.git xnu
git clone --branch i9100 https://github.com/kernel86-64/uniloader.git uniloader
cd uniloader
```

Run:

```sh
python3 scripts/build-i9100.py --xnu ../xnu --jobs 4
```

Default outputs in `out/`: raw **`zImage`**, matching **`mach_kernel.sys`** and
**`assym.s`**, and **`manifest.json`** with hashes, kernel UUID/entry and source
identity. Keep these together for debugging. The build generates a minimal
Apple device tree with `chosen/display-scale` as native uint32 1, creates an
empty ramdisk, selects `i9100_defconfig`, and rebuilds the loader. It replaces
the generated `.config`. The kernel entry comes from `LC_UNIXTHREAD` rather
than the stale configuration fallback offset.

Use `--skip-kernel` only with an already built, matching kernel and symbols.
`--archives` additionally creates `boot.img`, `zImage.tar` and `boot.tar`.
Default raw builds leave any previously generated archives untouched; select
artifacts from the current manifest. No rootfs or Apple shared cache is embedded.

## Device status

HUD32 keeps only GPU, BAT and LIVE IRQ in the runtime overlay, with one extra
GPU detail row on failure. It retains the GPU31 self-test and input/trace path.

The phone boots iOS 7 with working touch and a software display path. Home and
running-kernel charger services are enabled. Complete charging and long-term
stability remain unverified; random SpringBoard exits and limited speed persist.
Mali hardware tests confirm clear/geometry and PP0 texture upload/sample/update.
GPU31 fixes a clear-color channel swap exposed by GPU30's first alpha blend;
the corrected blend and all4 PP passed on the phone. The new MALI33 userspace
transport/client is separate and awaits its own phone validation. iOS GLES/EAGL and
GPU-accelerated SpringBoard are not implemented.

For Download Mode, the raw artifact can be flashed with the existing command:

```sh
heimdall flash --KERNEL out/zImage
```

This build tool does not flash a device. It targets **GT-I9100 only**; recovery,
powered-off charging, audio, radios and suspend/resume are not implemented or
verified. See the sibling XNU repository's `docs/GT-I9100.md` for board notes.
Source publication is separate from a combined binary release: component
licenses, including the XNU port's GPL thermistor data, need review before
redistributing a built kernel. No Apple userspace, SDKs, firmware or rootfs is
included here.

GPU and related development reports: [progress archive](docs/progress/README.md).
