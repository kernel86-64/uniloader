#!/usr/bin/env python3
import struct
import sys
import os

BOOT_MAGIC = b"ANDROID!"
BOOT_PAGE_SIZE = 2048

def make_boot_img(kernel_path="uniloader/uniLoader", output_path="boot.img", base=0x40000000, cmdline=""):
    with open(kernel_path, "rb") as f:
        kernel_data = f.read()

    kernel_size = len(kernel_data)
    ramdisk_size = 0

    kernel_addr  = base + 0x00008000  # 0x40008000
    ramdisk_addr = base + 0x02000000  # 0x42000000
    second_addr  = base + 0x00f00000
    tags_addr    = base + 0x00000100  # 0x40000100
    page_size    = BOOT_PAGE_SIZE

    def pad(data, ps):
        rem = len(data) % ps
        if rem != 0:
            return data + b"\x00" * (ps - rem)
        return data

    header = struct.pack(
        "<8s10I16s512s8I",
        BOOT_MAGIC,
        kernel_size,
        kernel_addr,
        ramdisk_size,
        ramdisk_addr,
        0,              # second_size
        second_addr,    # second_addr
        tags_addr,
        page_size,
        0, 0,           # unused[2]
        b"uniLoader-i9100"[:16].ljust(16, b"\x00"),
        cmdline.encode("ascii")[:512].ljust(512, b"\x00"),
        0, 0, 0, 0, 0, 0, 0, 0 # id[8]
    )
    padded_hdr = pad(header, page_size)
    padded_kernel = pad(kernel_data, page_size)

    with open(output_path, "wb") as f:
        f.write(padded_hdr)
        f.write(padded_kernel)

    print(f"Generated Android boot image: {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Package uniLoader as an Android boot image")
    parser.add_argument("kernel")
    parser.add_argument("output")
    args = parser.parse_args()
    make_boot_img(args.kernel, args.output)
