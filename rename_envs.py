import os
import re
import sys
    
def rename_files(root_dir: str):
    env_dir = os.path.join(root_dir, "env")

    if (os.path.exists(root_dir) == False):
        print("ERROR: Location " + root_dir + " doesn't exist")
        return
    
    if (os.path.exists(env_dir) == False):
        print("ERROR: Location " + env_dir + " doesn't point to root directory (couldn't find /env)")

    pattern = re.compile("\d{4}")

    for file in [
        os.path.join(parts[0], file) 
        for parts in os.walk(env_dir) if len(parts[2]) != 0 
        for file in parts[2] if file.lower().endswith(".env")
        ]:
        file_name = os.path.basename(file)
        result = pattern.search(file_name)
        if result != None:
            name_span = result.span()
            env_id = int(file_name[name_span[0]:name_span[1]])
            if env_id < 1000:
                new_name = os.path.join(
                    os.path.dirname(file),
                    file_name[:name_span[0]] + str(env_id).zfill(3) + file_name[name_span[1]:]
                )
                os.rename(file, new_name)
                print(new_name)

def main():
    # make sure directory is PS3_GAME/USRDIR
    if len(sys.argv) < 2:
        print("Missing folder (should point to June 2014 PS3_GAME/USRDIR)")
        return
    # enums in P5 2014 only have 3 digits for major ID
    rename_files(sys.argv[1])
    

if __name__ == "__main__":
    main()