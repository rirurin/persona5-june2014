from alpha3_utils import *
import io
import os
import struct
import sys

# TYPE 1
class PacFile:
    name: str
    data: bytes
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def stream_read(file: io.BufferedReader):
        filename = str(file.read(32), "ASCII").strip("\0")
        filesize, = StructExtensions.read(file, ">I")
        filedata = file.read(filesize)
        return PacFile(filename, filedata)
    def stream_write(self, file: io.BytesIO):
        bname = bytes(self.name, "ASCII")
        file.write(bname)
        file.write(bytes(32 - bname.count()))
        file.write(self.data)

class PacArchive:
    files: dict[str, PacFile]
    def __init__(self, files):
        self.files = files

    def stream_read(file : io.BufferedReader):
        file_count = int(StructExtensions.read(file, ">I")[0])
        files = {}
        for _ in range(file_count):
            new_file : PacFile = PacFile.stream_read(file)
            print(new_file.name)
            files[new_file.name] = new_file
        file.close()
        return PacArchive(files)
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">I", self.files.__len__()))
        for f in self.files.values():
            bname = bytes(f.name, "ASCII")
            file.write(bname)
            file.write(bytes(32 - bname.__len__()))
            file.write(struct.pack(">I", len(f.data)))
            file.write(f.data)
        file.close()
            
    
# TYPE 2
class PakFile:
    name: str
    data: bytes
    def __init__(self, name, data):
        self.name = name
        self.data = data
    def stream_read(file: io.BufferedReader):
        FileExtensions.alignto(file, 64)
        filename = str(file.read(252), "ASCII", errors="ignore").strip("\0")
        filesize, = StructExtensions.read(file, "<I")
        filedata = None
        if filesize > 0:
            filedata = file.read(filesize)
        return PakFile(filename, filedata)
    def stream_write(self, file: io.BytesIO):
        file.write(self.data)

class PakArchive:
    files: dict[str, PakFile]
    def __init__(self, files):
        self.files = files

    def stream_read(file: io.BufferedReader):
        file.seek(0, 2)
        filesize = file.tell()
        file.seek(0, 0)
        files = {}
        while file.tell() < filesize:
            new_file: PakFile = PakFile.stream_read(file)
            if new_file.data != None:
                print(new_file.name)
                files[new_file.name] = new_file
        file.close()
        return PakArchive(files)

def main():
    # Test
    if len(sys.argv) < 2:
        print("Missing PAC type")
        return
    if len(sys.argv) < 3:
        print("Missing PAC archive location")
        return
    pactype = int(sys.argv[1])
    filename = sys.argv[2]
    if os.path.exists(filename) == False:
        raise Exception("File at " + filename + " doesn't exist")
    match pactype:
        case 1:
            PacArchive.stream_read(open(filename, "rb"))
        case 2:
            PakArchive.stream_read(open(filename, "rb"))
        case _:
            raise Exception("Unknown PAC type " + str(pactype))

if __name__ == "__main__":
    main()