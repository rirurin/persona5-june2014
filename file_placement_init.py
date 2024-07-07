from alpha3_utils import *
from binary_flow import *
from pac_archive import *
import create_ftds

import io
import os
import shutil
import struct
import sys

def move_eboot(eboot_dir):
    # Move swordtrack/SW.bin into EBOOT.bin
    FileExtensions.copy_file(
        os.path.join(eboot_dir, "PS3_GAME/USRDIR/swordtrack/SW.BIN"),
        os.path.join(eboot_dir, "EBOOT.BIN")
    )

def add_ftd_to_pac(ftd_name: str, pac_archive: PacArchive):
    buf = io.BytesIO()
    new_ftd = create_ftds.Ftd(0x10000)
    new_ftd.serialize(buf)
    pac_archive.files[ftd_name] = PacFile(ftd_name, buf.read())

def place_files(root_dir):
    # Run create_ftds.py to create the necessary FTD files
    create_ftds.create_ftds(root_dir)
    # Copy init/msg_combine_lvup.bmd into P4G/facility/msg_combine_lvup.bmd
    init_dir = FileExtensions.checked_dir(root_dir, "init")
    p4g_faclty_dir = FileExtensions.checked_dir(root_dir, "P4G/facility")
    FileExtensions.copy_file(
        os.path.join(init_dir, "msg_combine_lvup.bmd"),
        os.path.join(p4g_faclty_dir, "msg_combine_lvup.bmd"))
    # Create crowd2d_05.dds and crowd2d_06.dds as a copy of crowd2d_01.dds from field/npc, put into field/panel/wipe
    fldnpc_dir = FileExtensions.checked_dir(root_dir, "field/npc")
    fldwipe_dir = FileExtensions.checked_dir(root_dir, "field/panel/wipe")
    FileExtensions.copy_file(
        os.path.join(fldnpc_dir, "crowd2d_01.dds"),
        os.path.join(fldwipe_dir, "crowd2d_05.dds")
    )
    FileExtensions.copy_file(
        os.path.join(fldnpc_dir, "crowd2d_01.dds"),
        os.path.join(fldwipe_dir, "crowd2d_06.dds")
    )
    # Replace init/fclTable.bin and init/datMsg.pak
    fclTblBinName = os.path.join(init_dir, "fclTable.bin")
    fclTblBin: PacArchive = PacArchive.stream_read(open(fclTblBinName, "rb"))
    if fclTblBin.files.__len__() == 0x6a:
        add_ftd_to_pac("fclCombineBirthMessage.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineGetPTMessage.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineTable_Fifth.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineTable_Fourth.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineTable_Sixth.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineTable_ThirdSP.ftd", fclTblBin)
        add_ftd_to_pac("fclCombineTable_Twelfth.ftd", fclTblBin)
        add_ftd_to_pac("fclComuLvExp.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_CELL2.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_COMBINE.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_ELVGIRL.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_ELVGIRL_ROOT.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_LIVER.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_SKLCARD_ROOT.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_SKLCARD0.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_SKLCARD1.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_SKLCARD2.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_USERCMM_ROOT.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_USERCMM0.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_USERCMM1.ftd", fclTblBin)
        add_ftd_to_pac("fclHelpTable_USERCMM2.ftd", fclTblBin)
        add_ftd_to_pac("fclMarieEvtTable.ftd", fclTblBin)
        add_ftd_to_pac("fclSklCardText.ftd", fclTblBin)
        fclTblBin.stream_write(open(fclTblBinName, "wb"))
        print("Updated fclTable.bin")
    else:
        print("fclTable.bin was already modified")
    # TODO
    # datMsg.pak: Create dummy datQuestReward.bmd by copying msg_combine_lvup.bmd
    datMsgPakName = os.path.join(init_dir, "datMsg.pak")
    datMsgPak: PacArchive = PacArchive.stream_read(open(datMsgPakName, "rb"))
    if datMsgPak.files.__contains__("datQuestReward.bmd"):
        print("datQuestReward already exists")
    else:
        msgcmb: io.BufferedReader = open(os.path.join(init_dir, "msg_combine_lvup.bmd"), "rb")
        datMsgPak.files["datQuestReward.bmd"] = PacFile("datQuestReward.bmd", msgcmb.read())
        datMsgPak.stream_write(open(datMsgPakName, "wb"))
        print("Updated datMsg.pak")
    # Move init/cmm.bin into P4G/init/cmm.bin
    p4g_init_dir = FileExtensions.checked_dir(root_dir, "P4G/init")
    FileExtensions.copy_file(
        os.path.join(init_dir, "cmm.bin"),
        os.path.join(p4g_init_dir, "cmm.bin")
    )
    # Extract init/evtWipeTex.pak, move into test/ikeda/wipe/
    evtwipetex: PakArchive = PakArchive.stream_read(open(FileExtensions.checked_dir(init_dir, "evtWipeTex.pak"), "rb"))
    ikedawipe_dir = FileExtensions.make_dir_checked(os.path.join(root_dir, "test/ikeda/wipe"))
    evtwipetex.files['test.dds'].stream_write(open(os.path.join(ikedawipe_dir, "test.dds"), "wb"))
    evtwipetex.files['test2.dds'].stream_write(open(os.path.join(ikedawipe_dir, "test2.dds"), "wb"))
    # rename p5_field_day.spd to fld.spd
    calendar_dir = FileExtensions.checked_dir(root_dir, "calendar")
    FileExtensions.copy_file(
        os.path.join(calendar_dir, "p5_field_day.spd"),
        os.path.join(calendar_dir, "fld.spd")
    )
    # create blank cldResult.bmd and cldresult.bf
    FileExtensions.copy_file(
        os.path.join(init_dir, "msg_combine_lvup.bmd"),
        os.path.join(calendar_dir, "cldResult.bmd")
    )
    samplescr_dir = FileExtensions.checked_dir(root_dir, "sample/script")
    FileExtensions.copy_file(
        os.path.join(samplescr_dir, "test.bf"),
        os.path.join(calendar_dir, "cldresult.bf")
    )
    # rename day.plg to cldDate.plg
    FileExtensions.copy_file(
        os.path.join(calendar_dir, "day.plg"),
        os.path.join(calendar_dir, "cldDate.plg")
    )
    # copy font/icon.dds to resident/icon.dds
    font_dir = FileExtensions.checked_dir(root_dir, "font")
    resident_dir = FileExtensions.checked_dir(root_dir, "resident")
    FileExtensions.copy_file(
        os.path.join(font_dir, "icon.dds"),
        os.path.join(resident_dir, "icon.dds")
    )

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to directory containing EBOOT.BIN)")
        return
    root = sys.argv[1]
    move_eboot(root)
    file_root = FileExtensions.checked_dir(root, "PS3_GAME/USRDIR")
    place_files(FileExtensions.checked_dir(file_root, None))
    

if __name__ == "__main__":
    main()