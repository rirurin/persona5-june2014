import os
import sys
import struct

# convert newer Persona 5 roadmap files to June 2014 compatible ones

def main():
    if len(sys.argv) < 2:
        print("Error: Missing filename")
        return
    
    filename = os.path.basename(sys.argv[1])
    filesize = os.stat(sys.argv[1]).st_size
    file = open(sys.argv[1], "rb")
    match filename:
        case "roadmap.bin":
            rmap_entry_count = int(filesize / 0x10)
            print("input file is " + str(filesize) + " bytes, " + str(rmap_entry_count) + " entries")
            rmap_out_file = os.path.splitext(sys.argv[1])[0] + "_out.bin"
            roadmap_fileout = open(rmap_out_file, "wb")
            for i in range(rmap_entry_count):    
                rmap_in = struct.unpack("<4H2I", file.read(16)) # size 0x10
                rmap_out = struct.pack("<4HI", rmap_in[0], rmap_in[1], rmap_in[2], rmap_in[3], rmap_in[4]) # size 0xc
                roadmap_fileout.write(rmap_out)
        case "texpack.bin":
            tex_entry_count = int(filesize / 0x68)
            print("input file is " + str(filesize) + " bytes, " + str(tex_entry_count) + " entries")
            tex_out_file = os.path.splitext(sys.argv[1])[0] + "_out.bin"
            tex_fileout = open(tex_out_file, "wb")
            for i in range(tex_entry_count):
                tex_in = struct.unpack("<2HIf23I", file.read(0x68))
                tex_out = struct.pack("<2HIfI", tex_in[0], tex_in[1], tex_in[2], tex_in[3], tex_in[4]) # size 0x10
                tex_fileout.write(tex_out)
        case _:
            print("Error: unimplemented file " + filename)


if __name__ == "__main__":
    main()