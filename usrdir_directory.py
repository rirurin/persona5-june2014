import os
import shutil
import sys

class USRDIR_Directory:
    def __init__(self, path):
        if (os.path.exists(path) == False):
            raise Exception("ERROR: Location " + path + " doesn't exist")
        self.root_path = path
        self.inner_paths = set()

    def add_inner_path(self, path: list):
        new_inner_path = os.path.join(self.root_path, *path)
        if (os.path.exists(new_inner_path) == False):
            raise Exception("ERROR: Location " + new_inner_path + " doesn't point to root directory (couldn't find " + path  + " )")
        self.inner_paths.add(new_inner_path)
        return new_inner_path

"""
def main():
    # make sure directory is PS3_GAME/USRDIR
    if len(sys.argv) < 2:
        print("Missing source folder (December 2015)")
        return
    new_path = USRDIR_Directory(sys.argv[1])
    print(new_path.add_inner_path(["field", "ftd"]))
    

if __name__ == "__main__":
    main()
"""