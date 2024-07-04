import io
import shutil
import struct
import os

class StructExtensions:
    # unpack from a file stream
    def read(file, sig):
        return struct.unpack(sig, file.read(struct.calcsize(sig)))
    
class FileExtensions:
    def alignto(file: io.BufferedReader, amount):
        align = file.tell() % amount
        if align == 0:
            return
        file.seek(amount - align, 1)

    def checked_dir(root, sub):
        dir = root
        if sub != None:
            dir = os.path.join(root, sub)
        if (os.path.exists(dir) == False):
            raise Exception("ERROR: Location " + dir + " doesn't exist")
        return dir

    def copy_file(src, dest):
        FileExtensions.checked_dir(src, None)
        if os.path.exists(dest):
            print(dest + " already exists")
        else:
            shutil.copy2(src, dest)
            print(src + " -> " + dest)

    def make_dir_checked(path) -> str:
        if os.path.exists(path) == False:
            os.makedirs(path)
        return path
    
class Vector2:
    def read(file):
        return StructExtensions.read(file, "<2f")
    def print(vec):
        print("< " + str(vec[0]) + "," + str(vec[1]) + " >")
    
class Vector3:
    def read(file):
        return StructExtensions.read(file, "<3f")
    def print(vec):
        print("< " + str(vec[0]) + "," + str(vec[1]) + "," + str(vec[2]) + " >")
    
class Vector4:
    def read(file):
        return StructExtensions.read(file, "<4f")
    def print(vec):
        print("< " + str(vec[0]) + "," + str(vec[1]) + "," + str(vec[2]) + "," + str(vec[3]) + " >")

class Matrix3x4:
    def read(file):
        return StructExtensions.read(file, "<12f")
    
class ByteColorRGB:
    def read(file):
        return StructExtensions.read(file, "<3B")
    
class ByteColorRGBA:
    def read(file):
        return StructExtensions.read(file, "<4B")