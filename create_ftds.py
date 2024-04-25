import io
import os
import sys
import struct

# handle making/modifying files used in field/ftd

def alignto(fhandle: io.BytesIO, val):
    alignment = val - fhandle.tell() % val
    if alignment != val:
        fhandle.write(bytes(alignment))

class Ftd:
    def __init__(self, field00):
        self.lists = []
        self.field00 = field00
        self.data_type = 0

    def extension():
        return "ftd"
    
    def magic():
        return "FTD0"

    def file_name(base):
        return base + "." + Ftd.extension()
    
    def header_sizeof():
        return 0x10
    
    def alignment():
        return 0x10
    
    def parse_from_filename(file, schemas: dict):
        fhandle = open(file, "rb")
        return Ftd.parse_from_handle(fhandle, schemas)

    # assumes that the file handle's position was set at the right offset in the caller
    def parse_from_handle(fhandle: io.BytesIO, schemas: dict):
        # read header
        ftdheader = struct.unpack(">3I2H", fhandle.read(Ftd.header_sizeof()))
        # read each list
        ftd_returned = Ftd(ftdheader[0])
        for i in range(ftdheader[4]):
            fhandle.seek(Ftd.header_sizeof() + i * 4)
            curr_offset = int.from_bytes(fhandle.read(4), byteorder="big")
            fhandle.seek(curr_offset) # relative to start of file
            if -1 in schemas == False:
                raise Exception("ERROR: FtdList schema dictionary missing default value")
            target_schema = schemas[i] if i in schemas else schemas[-1]
            ftd_returned.lists.append(FtdList.parse_from_handle(fhandle, target_schema))
        return ftd_returned
    
    def serialize(self, fhandle: io.BytesIO):
        # serialize header
        header_start = fhandle.tell()
        fhandle.write(self.field00.to_bytes(4, byteorder="big"))
        fhandle.write(bytes(Ftd.magic(), encoding="ASCII"))
        fhandle.write(bytes(4)) # file size
        fhandle.write(self.data_type.to_bytes(2, byteorder="big"))
        fhandle.write(len(self.lists).to_bytes(2, byteorder="big"))
        # data offsets go here
        if len(self.lists) > 0:
            fhandle.write(bytes(4 * len(self.lists)))
            list_offsets = []
            alignto(fhandle, Ftd.alignment())
            curr_list: FtdList
            for curr_list in self.lists:
                list_offsets.append(fhandle.tell())
                curr_list.serialize(fhandle)
            file_size_total = fhandle.tell()
            # write file size
            fhandle.seek(header_start + 8)
            fhandle.write(file_size_total.to_bytes(4, byteorder="big"))
            # write data offsets
            fhandle.seek(header_start + 0x10)
            for i in list_offsets:
                fhandle.write(i.to_bytes(4, byteorder="big"))
        else:
            fhandle.write(bytes(0x10))
            fhandle.seek(header_start + 8)
            fhandle.write(0x20.to_bytes(4, byteorder="big"))

class FtdList:
    def __init__(self, schema):
        self.field00 = 0
        self.entry_type = 0
        self.entries = []
        self.schema = schema

    def header_sizeof():
        return 0x10
    
    def alignment():
        return 0x10

    def parse_from_handle(fhandle: io.BytesIO, schema):
        # read header
        listheader = struct.unpack(">3I2H", fhandle.read(FtdList.header_sizeof()))
        entry_size = int(listheader[1] / listheader[2])
        if entry_size != struct.calcsize(schema):
            raise Exception("ERROR: FtdList schema " + str(schema) + " doesn't match entry size " + str(entry_size))
        list_returned = FtdList(schema)
        for i in range(listheader[2]):
            entry = struct.unpack(schema, fhandle.read(entry_size))
            list_returned.entries.append(entry)
        return list_returned
    
    def serialize(self, fhandle: io.BytesIO):
        # serialize header
        entry_size = struct.calcsize(self.schema)
        fhandle.write(self.field00.to_bytes(4, byteorder="big"))
        fhandle.write((entry_size * len(self.entries)).to_bytes(4, byteorder="big"))
        fhandle.write(len(self.entries).to_bytes(4, byteorder="big"))
        fhandle.write(self.entry_type.to_bytes(2, byteorder="big"))
        fhandle.write(bytes(2))
        # serialize entries
        for i in self.entries:
            fhandle.write(struct.pack(self.schema, *i))
        # align to 0x10
        alignto(fhandle, FtdList.alignment())

def serialize_empty_ftd(name, field_state_ftd):
    femptyftd = open(os.path.join("test_resources", Ftd.file_name(name)), "wb")
    Ftd(0x10000).serialize(femptyftd)

# these ftds were from a point in development where fldStateOnly was split into several lists
# each fldState is a 4 byte sequence of
# AAAA BBBB
# fld major, fld minor
field_state = "fldStateOnly"
non_existant_ftds = {
    "fldAlertGauge": serialize_empty_ftd,
    "fldCrouchOnly": serialize_empty_ftd,
    "fldEntranceNo": serialize_empty_ftd,
    "fldNotFollow": serialize_empty_ftd,
    "fldOutdoor": serialize_empty_ftd,
    "fldPlayerSpeed": serialize_empty_ftd,
    "fldPrisoner": serialize_empty_ftd,
    "fldWalkOnly": serialize_empty_ftd
}

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
    field_state_schemas = {-1: ">2BH"}
    field_state_ftd: Ftd = Ftd.parse_from_filename(os.path.join(ftd_dir, Ftd.file_name(field_state)), field_state_schemas)

    for exist_ftd in non_existant_ftds:
        non_existant_ftds[exist_ftd](exist_ftd, field_state_ftd)
    
    

if __name__ == "__main__":
    main()