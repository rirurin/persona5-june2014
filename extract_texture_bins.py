from alpha3_utils import *
from pac_archive import *
import sys

def extract_texture_bins(root_dir, output_dir):
    tex_dir = FileExtensions.checked_dir(root_dir, "model/field/textures")
    for file in [
         os.path.join(parts[0], file) 
         for parts in os.walk(tex_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".bin")
         ]:
        tex_dir = FileExtensions.make_dir_checked(os.path.join(output_dir, os.path.basename(file).split(".")[0]))
        print(os.path.join(tex_dir, file))
        texbinpack: PakArchive = PakArchive.stream_read(open(os.path.join(tex_dir, file), "rb"))
        for f in texbinpack.files.values():
            if f.name != None:
                print(f.name)
                new_file = open(os.path.join(tex_dir, f.name), "wb")
                new_file.write(f.data)
                new_file.close()

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to directory containing your EBOOT)")
        return
    if len(sys.argv) < 3:
        print("Error: Missing texture bin output directory")
        return
    file_root = FileExtensions.checked_dir(sys.argv[1], "PS3_GAME/USRDIR")
    extract_texture_bins(file_root, FileExtensions.checked_dir(sys.argv[2], None))
    

if __name__ == "__main__":
    main()