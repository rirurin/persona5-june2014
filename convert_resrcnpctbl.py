from alpha3_utils import *

import struct
import os
import sys

def convert_resrcnpctbl(root_dir):
    npctbl_bin = FileExtensions.checked_dir(root_dir, "resource/resrcNpcTbl.bin")
    print(npctbl_bin)
    # Alpha 5 resrcNpcTbl: 0x900c / 0x1c per entry = 0x525 entries
    a5_resrcnpctbl_sig = ">3H2B3H2B6H" # 16 parts
    # Alpha 3 resrcNpcTbl: 0x18 * 0x525 = 0x7b78
    a3_resrcnpctbl_sig = ">3H2BH2BH2B4H" # 15 parts
    filesize = os.path.getsize(npctbl_bin)
    read_file = open(npctbl_bin, "rb")
    resrc_entries = []
    for _ in range(int(filesize / struct.calcsize(a5_resrcnpctbl_sig))):
        resrc_entries.append(StructExtensions.read(read_file, a5_resrcnpctbl_sig))
    read_file.close()
    write_file = open(npctbl_bin, "wb")
    for npc in resrc_entries:
        print(str(npc[2]).zfill(4) + "_" + str(npc[3]).zfill(3) + "_" + str(npc[4]).zfill(3))
        npc_serial = struct.pack(a3_resrcnpctbl_sig, 
           npc[0], # index 
           npc[1], # reserve
           npc[2], # major
           npc[3], # minor
           npc[4], # sub
           npc[6], # attach_major
           0, # attach_minor TEMP
           # npc[7], # attach_minor
           npc[8], # umbrella
           npc[9], # attach_major2
           npc[10], # attach_minor2
           npc[11], # anim_type
           npc[12], # anim_base
           npc[13], # anim_add
           npc[14], # anim_base_rain
           npc[15], # anim_add_rain
        )
        write_file.write(npc_serial)
    write_file.close()

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    # Not needed
    # convert_resrcnpctbl(FileExtensions.checked_dir(sys.argv[1], None))

if __name__ == "__main__":
    main()