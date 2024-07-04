from alpha3_utils import *
from create_ftds import *
import sys

def add_text_entry(list: FtdList, text: str):
    item_name = bytes(text, "ASCII")
    item_name += bytes(64 - item_name.__len__())
    list.entries.append(item_name)

def cmptable(root_dir):
    init_dir = FileExtensions.checked_dir(root_dir, "init")
    cmp_equip_param = Ftd(0x10000)
    cmp_equip_param_list = FtdList("64B")
    add_text_entry(cmp_equip_param_list, "Attack")
    add_text_entry(cmp_equip_param_list, "Hit")
    add_text_entry(cmp_equip_param_list, "Defense")
    add_text_entry(cmp_equip_param_list, "Evasion")
    add_text_entry(cmp_equip_param_list, "Effect")
    cmp_equip_param.lists.append(cmp_equip_param_list)

    new_file = open(os.path.join(init_dir, "cmpEquipParam.ctd"), "wb")
    cmp_equip_param.serialize(new_file)
    new_file.close()


def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    cmptable(FileExtensions.checked_dir(sys.argv[1], None))
    

if __name__ == "__main__":
    main()