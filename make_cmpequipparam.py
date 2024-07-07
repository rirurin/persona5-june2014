from alpha3_utils import *
from create_ftds import *
from pac_archive import *
import sys

def add_text_entry(list: FtdList, text: str):
    item_name = bytes(text, "ASCII")
    item_name += bytes(64 - item_name.__len__())
    list.entries.append(item_name)

def create_status_files(root_dir):
    init_dir = FileExtensions.checked_dir(root_dir, "init")
    cmp_equip_param = Ftd(0x10000)
    cmp_equip_param_list = FtdList("64B")
    add_text_entry(cmp_equip_param_list, "Attack")
    add_text_entry(cmp_equip_param_list, "Hit")
    add_text_entry(cmp_equip_param_list, "Defense")
    add_text_entry(cmp_equip_param_list, "Evasion")
    add_text_entry(cmp_equip_param_list, "Effect")
    cmp_equip_param.lists.append(cmp_equip_param_list)

    cmp_equip_param_serial = io.BytesIO()
    cmp_equip_param.serialize(cmp_equip_param_serial)

    cmpTableBinName = FileExtensions.checked_dir(init_dir, "cmpTable.bin")
    cmpTableBin: PacArchive = PacArchive.stream_read(open(cmpTableBinName, "rb"))
    if cmpTableBin.files.__contains__("cmpEquipParam.ctd"):
        print("status: cmpTable was already edited")
    else:
        cmpTableBin.files["cmpEquipParam.ctd"] = PacFile("cmpEquipParam.ctd", cmp_equip_param_serial.read())
        cmpTableBin.stream_write(open(cmpTableBinName, "wb"))

def create_requests_files(root_dir):
    init_dir = FileExtensions.checked_dir(root_dir, "init")
    cmpTableBinName = FileExtensions.checked_dir(init_dir, "cmpTable.bin")
    cmpTableBin: PacArchive = PacArchive.stream_read(open(cmpTableBinName, "rb"))
    if cmpTableBin.files.__contains__("cmpQuestSortTable_MUST.ctd"):
        print("request: cmpTable was already edited")
    else:
        sortTableData = cmpTableBin.files["cmpQuestSortTable.ctd"].data
        cmpTableBin.files["cmpQuestSortTable_MUST.ctd"] = PacFile("cmpQuestSortTable_MUST.ctd", sortTableData)
        cmpTableBin.files["cmpQuestSortTable_URGENT.ctd"] = PacFile("cmpQuestSortTable_URGENT.ctd", sortTableData)
        cmpTableBin.files["cmpQuestSortTable_NORMAL.ctd"] = PacFile("cmpQuestSortTable_NORMAL.ctd", sortTableData)
        cmpTableBin.stream_write(open(cmpTableBinName, "wb"))

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    root_dir = FileExtensions.checked_dir(sys.argv[1], None)
    create_status_files(root_dir)
    create_requests_files(root_dir)

if __name__ == "__main__":
    main()