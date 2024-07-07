from alpha3_utils import *
import sys

def edit_facial(root_dir):
    face_dir = FileExtensions.checked_dir(root_dir, "battle/face")
    for filename in [
         os.path.join(parts[0], file) 
         for parts in os.walk(face_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".dat") and file.lower().startswith("bb")
         ]:
        print(filename)
        file = open(filename, "rb")
        facial_data = file.read()
        file.close()
        new_file = open(filename, "wb")
        new_file.write(struct.pack(">I", 3))
        new_file.write(facial_data[4:])
        new_file.close()

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to root directory)")
        return
    root = sys.argv[1]
    edit_facial(root)
    

if __name__ == "__main__":
    main()