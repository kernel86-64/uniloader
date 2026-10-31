#!/usr/bin/env python3
import struct
import sys

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Flatten XNU Mach-O segments for uniLoader")
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    src, dst = args.source, args.destination
    
    with open(src, "rb") as f:
        data = f.read()

    magic, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags = struct.unpack("<7I", data[:28])
    assert magic == 0xfeedface, f"Invalid magic: {hex(magic)}"

    offset = 28
    segments = []
    base_vmaddr = None
    max_vma = 0

    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack("<2I", data[offset:offset+8])
        if cmd == 1: # LC_SEGMENT
            segname = data[offset+8:offset+24].rstrip(b"\0").decode("ascii", "ignore")
            vmaddr, vmsize, fileoff, filesize = struct.unpack("<4I", data[offset+24:offset+40])
            segments.append((segname, vmaddr, vmsize, fileoff, filesize))
            if base_vmaddr is None or vmaddr < base_vmaddr:
                base_vmaddr = vmaddr
            if vmaddr + vmsize > max_vma:
                max_vma = vmaddr + vmsize
        offset += cmdsize

    total_size = max_vma - base_vmaddr
    print(f"Base vmaddr: {hex(base_vmaddr)}, Max vmaddr: {hex(max_vma)}, Total raw size: {total_size} bytes ({total_size / (1024*1024):.2f} MB)")

    raw = bytearray(total_size)
    for segname, vmaddr, vmsize, fileoff, filesize in segments:
        seg_off = vmaddr - base_vmaddr
        print(f"Segment {segname:16}: vmaddr={hex(vmaddr)} vmsize={hex(vmsize)} fileoff={fileoff} filesize={filesize} -> raw_off={hex(seg_off)}")
        if filesize > 0:
            raw[seg_off : seg_off + filesize] = data[fileoff : fileoff + filesize]

    with open(dst, "wb") as f:
        f.write(raw)

    print(f"Successfully wrote {dst} ({len(raw)} bytes)")

if __name__ == "__main__":
    main()
