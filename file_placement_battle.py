from alpha3_utils import *
from edit_facial import *
import sys

def place_files(root_dir):
    # battle/gui/btl_cmnd.GMD
    battlegui_dir = FileExtensions.checked_dir(root_dir, "battle/gui")
    FileExtensions.copy_file(
        os.path.join(battlegui_dir, "btl_menu_cmnd_front.GMD"),
        os.path.join(battlegui_dir, "btl_cmnd.GMD")
    )
    # edit facial data
    edit_facial(root_dir)
    # font/assist/jm_base.spd
    fldpanel_dir = FileExtensions.checked_dir(root_dir, "field/panel")
    fontassist_dir = FileExtensions.checked_dir(root_dir, "font/assist")
    FileExtensions.copy_file(
        os.path.join(fldpanel_dir, "p5minimap_01.spd"),
        os.path.join(fontassist_dir, "jm_base.spd")
    )
    # font/assist/jm_k003_00.spd
    fontassistch_dir = FileExtensions.checked_dir(fontassist_dir, "chara")
    FileExtensions.copy_file(
        os.path.join(fontassistch_dir, "003_00.spd"),
        os.path.join(fontassist_dir, "jm_k003_00.spd")
    )

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to directory containing EBOOT.bin)")
        return
    root = sys.argv[1]
    file_root = FileExtensions.checked_dir(root, "PS3_GAME/USRDIR")
    place_files(FileExtensions.checked_dir(file_root, None))
    

if __name__ == "__main__":
    main()