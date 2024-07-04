from alpha3_utils import *
from roadmaptbl import *
from pac_archive import *
import make_clt
import rename_envs

import sys

def place_files(root_dir):
    # env files need to be renamed from envXXXX_XXX_XXX to envXXX_XXX_XXX
    rename_envs.rename_files(root_dir)
    fldpanel_dir = FileExtensions.checked_dir(root_dir, "field/panel")
    # create field/panel/p5Wanted_01.spd
    # TODO
    # Create field/party/partyXX.bf for members 02 through 09
    # Find a better way to do this? Currently this just copies member.bf
    fldparty_dir = FileExtensions.checked_dir(root_dir, "field/party")
    for i in range(2, 10):
        FileExtensions.copy_file(
            os.path.join(fldparty_dir, "member.bf"),
            os.path.join(fldparty_dir, "party" + str(i).zfill(2) + ".bf")
        )

    # field/panel/check_test.spd
    # field/panel/PS3Pad_test.spd
    # field/panel/observation.spd

    # these are just blank files for now, if we find a good substitute later it can be replaced
    FileExtensions.copy_file(
        "blank.dds",
        os.path.join(fldpanel_dir, "dng_guide.dds")
    )
    FileExtensions.copy_file(
        "blank.dds",
        os.path.join(fldpanel_dir, "dokidokiheart.dds")
    )
    FileExtensions.copy_file(
        "blank.dds",
        os.path.join(fldpanel_dir, "telephone.dds")
    )

    # fix field npc/crowd
    make_clt.make_clt(root_dir)
    # copy phantom thief outfit 051_00 to 051_01
    for i in range(1, 10):
        idmajor = str(i).zfill(4)
        charmodel_dir = FileExtensions.checked_dir(root_dir, "model/character/" + idmajor)
        FileExtensions.copy_file(
            os.path.join(charmodel_dir, "c" + idmajor + "_051_00.GMD"),
            os.path.join(charmodel_dir, "c" + idmajor + "_051_01.GMD")
        )

    # split roadmap.tbl
    roadmap_dir = FileExtensions.checked_dir(root_dir, "field/panel/roadmap")
    roadmaptbl: PacArchive = PacArchive.stream_read(open(FileExtensions.checked_dir(roadmap_dir, "roadmap.tbl"), "rb"))
    roadmapbin = open(os.path.join(roadmap_dir, "roadmap.bin"), "wb")
    RoadmapBin.stream_read(io.BytesIO(roadmaptbl.files["roadmap.bin"].data)).stream_write(roadmapbin)
    texpackbin = open(os.path.join(roadmap_dir, "texpack.bin"), "wb")
    TexpackBin.stream_read(io.BytesIO(roadmaptbl.files["texpack.bin"].data)).stream_write(texpackbin)

    # create fe_kkmj_2 and fe_emy field EPLs (palace fields)
    fldepl_dir = FileExtensions.checked_dir(root_dir, "field/effect")

    FileExtensions.copy_file(
        os.path.join(fldepl_dir, "fe_kkmj_0.EPL"),
        os.path.join(fldepl_dir, "fe_kkmj_2.EPL")
    )
    FileExtensions.copy_file(
        os.path.join(fldepl_dir, "fe_emy_in.EPL"),
        os.path.join(fldepl_dir, "fe_emy.EPL")
    )

    # fixing up stuff for camp
    # move joker 2D portrait
    camp_dir = FileExtensions.checked_dir(root_dir, "camp")
    herotex_dir = FileExtensions.checked_dir(camp_dir, "herotex")
    for file in [
         os.path.join(parts[0], file) 
         for parts in os.walk(herotex_dir) if len(parts[2]) != 0 
         for file in parts[2] if file.lower().endswith(".dds")
         ]:
        FileExtensions.copy_file(
            file,
            os.path.join(camp_dir, os.path.basename(file))
        )

    # cmpEquipParam.ctd
    # FileExtensions.checked_dir(None)
    # Ftd(0x10000)
    # stats menu
    # this is from P4G, we'll have to rename it ourselves
    # TODO

def main():
    if len(sys.argv) < 2:
        print("Error: Missing root directory (should point to PS3_GAME/USRDIR)")
        return
    place_files(FileExtensions.checked_dir(sys.argv[1], None))
    

if __name__ == "__main__":
    main()