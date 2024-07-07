from alpha3_utils import *
from make_clt import PathNodeContainer

import os
import struct
import sys

# FLD_SHTTYPE_CONF
# FLD_SHTTYPE_POINT
# FLD_SHTTYPE_LINE
# type 4 doesn't exist in 2014
class ShtBase:
    def __init__(self, header, datas):
        self.header = header
        self.datas = datas
    
    def stream_read(file, header):
        raise Exception("Didn't implement stream_read!")
    
    def stream_write(self, file: io.BytesIO):
        raise Exception("Didn't implement stream_write!")
    
class ShtConfig(ShtBase):
    def stream_read(file: io.BytesIO, header):
        datas = file.read(0x100)
        return ShtConfig(header, datas)
    
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">4I", *self.header))
        file.write(self.datas)
    
class ShtPoint(ShtBase):
    def __init__(self, header, local_header, datas):
        self.header = header
        self.local_header = local_header
        self.datas = datas
    
    def stream_read(file, header):
        # 0x13040100 (alpha 3 ver)
        # 0x14092900
        # 0x15011000 (alpha 5 ver)
        ver = int(header[1])
        entries = StructExtensions.read(file, ">4I")
        datas = []
        for _ in range(entries[0]):
            datas.append(StructExtensions.read(file, ">2I5fI"))
            if ver >= 0x14092900:
                StructExtensions.read(file, ">I")
            if ver >= 0x15011000:
                StructExtensions.read(file, ">I")
        return ShtPoint(header, entries, datas)
    
    def stream_write(self, file: io.BytesIO):
        # self.header[1] = 0x13040100
        file.write(struct.pack(">4I", *self.header))
        file.write(struct.pack(">4I", *self.local_header))
        for f in self.datas:
            file.write(struct.pack(">2I5fI", *f))
    
class ShtLineEntry:
    nodes: PathNodeContainer
    def __init__(self, data, nodes):
        self.data = data
        self.nodes = nodes
    
class ShtLine(ShtBase):
    datas: list[ShtLineEntry]
    def __init__(self, header, local_header, datas):
        self.header = header
        self.local_header = local_header
        self.datas = datas
    # 0x14040800 (alpha 3 ver)
    # 0x14092900
    # 0x15011000 (alpha 5 ver)
    def stream_read(file, header):
        ver = int(header[1])
        entries = StructExtensions.read(file, ">4I")
        datas = []
        for _ in range(entries[0]):
            data = StructExtensions.read(file, ">I2fI")
            if ver >= 0x14092900:
                StructExtensions.read(file, ">I")
            if ver >= 0x15011000:
                StructExtensions.read(file, ">I")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(ShtLineEntry(data, nodes))
        return ShtLine(header, entries, datas)
    
    def stream_write(self, file: io.BytesIO):
        # self.header[1] = 0x14040800
        file.write(struct.pack(">4I", *self.header))
        file.write(struct.pack(">4I", *self.local_header))
        for f in self.datas:
            file.write(struct.pack(">I2fI", *f.data))
            file.write(struct.pack(">3I2H", *f.nodes.header))
            for n in f.nodes.nodes:
                file.write(struct.pack("<3f", *n))           

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    make_clt(FileExtensions.checked_dir(sys.argv[1], None))

def make_clt(root_dir):
    fldnpc_dir = FileExtensions.checked_dir(root_dir, "field/sht")
    for filename in [
         os.path.join(parts[0], file) 
         for parts in os.walk(fldnpc_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".sht") and file.lower().startswith("f") and file.lower().find("new") == -1
         ]:
        file = open(filename, "rb")
        filesize = os.path.getsize(filename)
        header = StructExtensions.read(file, ">4I")
        print(os.path.basename(filename) + ": " + hex(header[1]))
        sec_parts: list[ShtBase] = []
        while file.tell() < filesize:
            sec_header = StructExtensions.read(file, ">4I")
            print("section " + str(sec_header[0]) + ", ver " + hex(sec_header[1]))
            match sec_header[0]:
                case 1:
                    sec_parts.append(ShtConfig.stream_read(file, sec_header))
                case 2:
                    sec_parts.append(ShtPoint.stream_read(file, sec_header))
                case 3:
                    sec_parts.append(ShtLine.stream_read(file, sec_header))
                case _:
                    file.seek(int(sec_header[2]) - 0x10, 1)
        file.close()
        new_file = open(filename, "wb")
        new_file.write(struct.pack(">4I", *header))
        for p in sec_parts:
            p.stream_write(new_file)
        new_file.close()
        # print(sec_parts.__len__())

if __name__ == "__main__":
    main()