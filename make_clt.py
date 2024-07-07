from alpha3_utils import *

import os
import struct
import sys

# use to convert later CLTs
clt_type2_sig = ">I2HI10H3f2If"
clt_type2_ver = 0x14022500

class PathNodeContainer:
    def __init__(self, header, nodes):
        self.header = header
        self.nodes = nodes
    def stream_read(file):
        header = StructExtensions.read(file, ">3I2H")
        nodes = []
        for _ in range(header[3]):
            nodes.append(Vector3.read(file))
        return PathNodeContainer(header, nodes)
    
class CltEntries:
    def __init__(self, data, nodes):
        self.data = data
        self.nodes = nodes
        
class CltBase:
    def __init__(self, file, header, datas):
        self.file = file
        self.header = header
        self.datas = datas
    
    def stream_read(file, version, name):
        raise Exception("Didn't implement stream_read!")
    
    def stream_write(file):
        raise Exception("Didn't implement stream_write!")
    
    def is_supported(self):
        return True
    
class CltType1(CltBase):
    # Oldest supported version of CLT format
    # Early 2014 perhaps?
    # Used only in f000_000.CLT (ver 0x14021600)
    # 0x10 header, 0x30 entry
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">3I")
        print(name + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, ">I2HI10H3fI")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType1(file, header, datas)

class CltType2(CltBase):
    # Current CLT version used by June 2014
    # Used in several maps (ver 0x14022500)
    # 0x10 header, 0x38 entry
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">3I")
        print(name + ", version " + hex(version) + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, clt_type2_sig)
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType2(file, header, datas)

class CltType3(CltBase):
    # Used in f001_007.CLT and f013_006.CLT (ver 0x14102800)
    # First type too new for June 2014
    # 0x40 header. We can throw it all out
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">15I")
        print(name + ", version " + hex(version) + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, ">I2HI10H3f2If")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType3(file, header, datas)
    
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">I", clt_type2_ver))
        file.write(struct.pack(">3I", self.header[0], 0, 0))
        for d in self.datas:
            file.write(struct.pack(clt_type2_sig, *d.data))
            file.write(struct.pack(">3I2H", *d.nodes.header))
            for n in d.nodes.nodes:
                file.write(struct.pack("<3f", *n))
    
    def is_supported(self):
        return False

class CltType4(CltBase):
    # 0x44 header, same as before
    # data section is still the same
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">16I")
        print(name + ", version " + hex(version) + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, ">I2HI10H3f2If")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType4(file, header, datas)
    
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">I", clt_type2_ver))
        file.write(struct.pack(">3I", self.header[0], 0, 0))
        for d in self.datas:
            file.write(struct.pack(clt_type2_sig, *d.data))
            file.write(struct.pack(">3I2H", *d.nodes.header))
            for n in d.nodes.nodes:
                file.write(struct.pack("<3f", *n))

    def is_supported(self):
        return False

class CltType5(CltBase):
    # first significant changes to the data section
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">16I")
        print(name + ", version " + hex(version) + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, ">I2H3I10H3f2If")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType5(file, header, datas)
    
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">I", clt_type2_ver))
        file.write(struct.pack(">3I", self.header[0], 0, 0))
        for d in self.datas:
            file.write(struct.pack(
                clt_type2_sig, 
                d.data[0], # 13
                d.data[1], # 0
                d.data[2], # 0
                d.data[5], # 1
                d.data[6], # 324
                d.data[7], # 100
                d.data[8], # 0
                d.data[9], # 0
                d.data[10], # 0
                d.data[11], # 0
                d.data[12], # 0
                d.data[13], # 0
                d.data[14], # 0
                d.data[15], # 0
                d.data[16], # -0.9999999403953552
                d.data[17], # 0.0
                d.data[18], # -1.2688051498344066e-08
                d.data[19], # 195069184
                d.data[20], # 0
                d.data[21], # 0.0
            ))
            file.write(struct.pack(">3I2H", *d.nodes.header))
            for n in d.nodes.nodes:
                file.write(struct.pack("<3f", *n))

    def is_supported(self):
        return False

class CltType6(CltBase):
    # version 0x15111200 - latest version used in December 2015
    def stream_read(file, version, name):
        header = StructExtensions.read(file, ">16I")
        print(name + ", version " + hex(version) + ", count " + str(header[0]))
        datas = []
        for _ in range(header[0]):
            data = StructExtensions.read(file, ">I2H5I10H3f2If")
            nodes = PathNodeContainer.stream_read(file)
            datas.append(CltEntries(data, nodes))
        return CltType6(file, header, datas)
    
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">I", clt_type2_ver))
        file.write(struct.pack(">3I", self.header[0], 0, 0))
        for d in self.datas:
            file.write(struct.pack(
                clt_type2_sig, 
                d.data[0], # 5
                d.data[1], # 6
                d.data[2], # 0
                d.data[7], # 1
                d.data[8], # 324
                d.data[9], # 100
                d.data[10], # 0
                d.data[11], # 0
                d.data[12], # 0
                d.data[13], # 0
                d.data[14], # 0
                d.data[15], # 0
                d.data[16], # 0
                d.data[17], # 0
                d.data[18], # -0.9999999403953552
                d.data[19], # 0.0
                d.data[20], # -1.2688051498344066e-08
                d.data[21], # 195069184
                d.data[22], # 0
                d.data[23], # 0.0
            ))
            file.write(struct.pack(">3I2H", *d.nodes.header))
            for n in d.nodes.nodes:
                file.write(struct.pack("<3f", *n))

    def is_supported(self):
        return False


def make_clt(root_dir):
    fldnpc_dir = FileExtensions.checked_dir(root_dir, "field/npc")
    for filename in [
         os.path.join(parts[0], file) 
         for parts in os.walk(fldnpc_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".clt") and file.lower().startswith("f") and file.lower().find("new") == -1
         ]:
        file = open(filename, "rb")
        version, = StructExtensions.read(file, ">I")
        clt: CltBase = None
        match version:
            case version if version < 0x14022500:
                clt = CltType1.stream_read(file, version, filename)
            case version if version < 0x14102800:
                clt = CltType2.stream_read(file, version, filename)
            case version if version < 0x15041600:
                clt = CltType3.stream_read(file, version, filename)
            case version if version < 0x15052600:
                clt = CltType4.stream_read(file, version, filename)
            case version if version < 0x15111200:
                clt = CltType5.stream_read(file, version, filename)
            case _:
                clt = CltType6.stream_read(file, version, filename)
        if clt.is_supported() == False:
            # TEST
            # new_name = os.path.join(os.path.dirname(filename), os.path.basename(filename).split(".")[0] + "_NEW.CLT")
            new_name = filename
            new_file = open(new_name, "wb")
            clt.stream_write(new_file)
            new_file.close()
        file.close()

def list_clt(root_dir):
    fldnpc_dir = FileExtensions.checked_dir(root_dir, "field/npc")
    for filename in [
         os.path.join(parts[0], file) 
         for parts in os.walk(fldnpc_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".clt") and file.lower().startswith("f") and file.lower().find("new") == -1
         ]:
        file = open(filename, "rb")
        version, = StructExtensions.read(file, ">I")
        print(os.path.basename(filename) + ": " + hex(version))


def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    list_clt(FileExtensions.checked_dir(sys.argv[1], None))
    

if __name__ == "__main__":
    main()