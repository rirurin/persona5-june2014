import os
import sys
import struct

def main():
    if len(sys.argv) < 2:
        print("Error: Missing filename")
        return
    filename = os.path.basename(sys.argv[1])
    filesize = os.stat(sys.argv[1]).st_size
    file = open(sys.argv[1], "rb")
    entries_in = int(filesize / 0x30)
    # convert 2015 entries (0x30) to 2014 entries (0x44)
    # they include an extra u32[5] for materials
    print("got " + str(entries_in) + " entries")
    # read each entry, then spit out new one
    out_filename = os.path.splitext(sys.argv[1])[0] + "_out.bin"
    out_file = open(out_filename, "wb")
    for i in range(entries_in):
        curr_entry = file.read(0x30)
        out_file.write(curr_entry)
        out_file.write(bytes(20))
    # equip_info = struct.unpack("<3IH2B", file.read(0x10))
    # print(equip_info[0], equip_info[1], equip_info[2], equip_info[3], equip_info[4], equip_info[5])
    # weapon_stats = struct.unpack("<2H", file.read(0x4))
    # print(weapon_stats[0], weapon_stats[1])
    
    """for i in range(entries_in):
        print(equip_info[0], equip_info[1], equip_info[2], equip_info[3], equip_info[4], equip_info[5])
        weapon_entry_in = struct.unpack("<2H5B5H2I2BH", file.read(0x20))
        print(weapon_entry_in[0], weapon_entry_in[1])
        # materials = [0 for i in range(5)]
        # weapon_entry_out = struct.pack("<4HI", rmap_in[0], rmap_in[1], rmap_in[2], rmap_in[3], rmap_in[4])
        # out_file.write(rmap_out)
    """
    
if __name__ == "__main__":
    main()