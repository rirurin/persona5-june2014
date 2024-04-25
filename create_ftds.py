import os
import sys
import struct

# handle making/modifying files used in field/ftd

class Ftd:
    def __init__(self, field00, count):
        self.lists = []
        self.field00 = field00
        self.count = count

    def extension():
        return "ftd"

    def file_name(base):
        return base + "." + Ftd.extension()
    
    def header_sizeof():
        return 0x10
    
    def parse_from_filename(file):
        fhandle = open(file, "rb")
        Ftd.parse_from_handle(fhandle)

    # assumes that the file handle's position was set at the right offset in the caller
    def parse_from_handle(fhandle):
        # read header
        ftdheader = struct.unpack(">3I2H", fhandle.read(Ftd.header_sizeof()))
        # read each list
        for i in range(ftdheader[4]):
            fhandle.seek(Ftd.header_sizeof() + i * 4)
            curr_offset = int.from_bytes(fhandle.read(4), byteorder="big")
            fhandle.seek(curr_offset) # relative to start of file
            FtdList.parse_from_handle(fhandle)
        # newftd = Ftd(ftdheader[0], ftdheader[4])
        # return newftd

class FtdList:
    def __init__(self):
        self.entries = []

    def header_sizeof():
        return 0x10

    def parse_from_handle(fhandle):
        # read header
        listheader = struct.unpack(">3I2H", fhandle.read(FtdList.header_sizeof()))
        entry_size = int(listheader[1] / listheader[2])
        for i in range(listheader[2]):
            entry = struct.unpack(field_state_entry_unpack, fhandle.read(struct.calcsize(field_state_entry_unpack)))
            print(entry[0], entry[1])
        # print(str(entry_count) + " entries")

class FtdEntry:
    def __init__(self, schema):
        self.schema = schema

    def get_serialized_size(self):
        return struct.calcsize(self.schema)

# these ftds were from a point in development where fldStateOnly was split into several lists
# each fldState is a 4 byte sequence of
# AAAA BBBB
# fld major, fld minor
field_state = "fldStateOnly"
field_state_entry_unpack = ">2BH"
non_existant_ftds = [
    "fldAlertGauge",
    "fldCrouchOnly",
    "fldEntranceNo",
    "fldNotFollow",
    "fldOutdoor",
    "fldPlayerSpeed"
    "fldPrisoner",
    "fldWalkOnly"
]

def main():
    # make sure directory is PS3_GAME/USRDIR
    if len(sys.argv) < 2:
        print("Missing root folder location")
        return
    
    rootdir = sys.argv[1]
    ftd_dir = os.path.join(rootdir, "field", "ftd")

    if (os.path.exists(rootdir) == False):
        print("ERROR: Location " + rootdir + " doesn't exist")
        return
    # Assume that field/ftd was created in an earlier script
    if (os.path.exists(ftd_dir) == False):
        print("ERROR: Location " + rootdir + " doesn't point to root directory (couldn't find field/ftd)")

    exists_ftds = os.listdir(ftd_dir)
    # check fldStateOnly exists, then read it
    try:
        exists_ftds.index(Ftd.file_name(field_state))
    except:
        print("ERROR: Could not find file " + Ftd.file_name(field_state))
        return
    Ftd.parse_from_filename(os.path.join(ftd_dir, Ftd.file_name(field_state)))
    # for exist_ftd in exists_ftds:
    #     print(exist_ftd + " (" + str(os.path.getsize(os.path.join(ftd_dir, exist_ftd))) + " bytes)")

if __name__ == "__main__":
    main()