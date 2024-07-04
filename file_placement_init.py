from alpha3_utils import *
from binary_flow import *
from pac_archive import *
import create_ftds

import io
import os
import shutil
import struct
import sys

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
    # fclTable.bin:
    # fclCombineBirthMessage.ftd
    # fclCombineGetPTMessage.ftd
    # fclCombineTable_Fifth.ftd
    # fclCombineTable_Fourth.ftd
    # fclCombineTable_Sixth.ftd
    # fclCombineTable_ThirdSP.ftd
    # fclCombineTable_Twelfth.ftd
    # fclComuLvExp.ftd
    # fclHelpTable_CELL2.ftd
    # fclHelpTable_COMBINE.ftd
    # fclHelpTable_ELVGIRL.ftd
    # fclHelpTable_ELVGIRL_ROOT.ftd
    # fclHelpTable_LIVER.ftd
    # fclHelpTable_SKLCARD_ROOT.ftd
    # fclHelpTable_SKLCARD0.ftd
    # fclHelpTable_SKLCARD1.ftd
    # fclHelpTable_SKLCARD2.ftd
    # fclHelpTable_USERCMM_ROOT.ftd
    # fclHelpTable_USERCMM0.ftd
    # fclHelpTable_USERCMM1.ftd
    # fclHelpTable_USERCMM2.ftd
    # fclMarieEvtTable.ftd
    # fclSklCardText.ftd
    # TODO
    # datMsg.pak: Create dummy datQuestReward.bmd
    # TODO
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
    # create blank cldResult.bmd and cldResult.bf
    # TODO
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
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    place_files(FileExtensions.checked_dir(sys.argv[1], None))
    

if __name__ == "__main__":
    main()