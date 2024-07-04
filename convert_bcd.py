from alpha3_utils import *
import io
import os
import sys
import struct

# See https://github.com/tge-was-taken/010-Editor-Templates/blob/master/templates/p5r_bcd.bt

class NonZeroedString:
    def read(file):
        length, = StructExtensions.read(file, "B")
        return str(file.read(length), "ASCII")
    
# Note: InterpolateType is uint

class BCDSectionBase:
    def __init__(self, file, header, version):
        self.file = file
        self.header = header
        self.version = version
    
    def read(self):
        raise Exception("shouldn't be making an instance of the base type")

    def is_valid(self): 
        return True

class BCDSectionBase_NOTINALPHA3(BCDSectionBase):
    def is_valid(self): 
        return False

class BCDSection_BCDPlay(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)

class BCDSection_Unit_Anim(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2BfIf")

class BCDSection_EPL(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)

class BCDSection_EPL_Coordinate(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        Vector3.read(self.file)

class BCDSection_Unit_crdSet(BCDSectionBase):
    def read(self):
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<f")
    
class BCDSection_Unit_move(BCDSectionBase):
    def read(self):
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<If")

class BCDSection_Unit_rot(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<f")

class BCDSection_Unit_rotPos(BCDSectionBase):
    def read(self):
        Vector3.read(self.file)

class BCDSection_Unit_homePos(BCDSectionBase):
    def read(self):
        pass

class BCDSection_Cam(BCDSectionBase):
    def read(self):
        Vector3.read(self.file) # cameraLocation
        Vector3.read(self.file) # cameraTarget

class BCDSection_Unit_Culled(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")

class BCDSection_Cam_overview(BCDSectionBase):
    def read(self):
        pass

class BCDSection_EPL_Ex(BCDSectionBase):
    def read(self):
        BCDSection_EPL_Ex.read_inner(self.file)
    def read_inner(file):
        NonZeroedString.read(file)
        Vector3.read(file)
        StructExtensions.read(file, "<2f")

class BCDSection_Env_bright(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<f5B")

class BCDSection_Fld_color(BCDSectionBase):
    def read(self):
        ByteColorRGBA.read(self.file)

class BCDSection_Fld_HDR(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<f")
        
class BCDSection_Env_saturation(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<I2B")
        if self.version >= 0x9050000:
            StructExtensions.read(self.file, "<3B")

class BCDSection_Unit_DyingCulled(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")

class BCDSection_Cam_chant(BCDSectionBase):
    def read(self):
        pass

class BCDSection_Cam_move(BCDSectionBase):
    def read(self):
        Matrix3x4.read(self.file)
        StructExtensions.read(self.file, "<I") # interpolate

class BCDSection_Cam_goto(BCDSectionBase):
    def read(self):
        Vector3.read(self.file) # cameraLocation
        Vector3.read(self.file) # cameraTarget
        StructExtensions.read(self.file, "<I") # interpolate

class BCDSection_Cam_Chara(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)
    def read_inner(file, version):
        StructExtensions.read(file, "<3f")
        if version >= 0x8060100:
            StructExtensions.read(file, "<I")
        StructExtensions.read(file, "<fI")

class BCDSection_Cam_Chara_goto(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)

class BCDSection_Cam_Chara_fixed(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)

class BCDSection_Cam_Chara_look(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)
        StructExtensions.read(self.file, "<I")

class BCDSection_Cam_Chara_view(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)
        StructExtensions.read(self.file, "<I")

class BCDSection_Unit_pathMove(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<2f2BIf")
        if self.version >= 0x9020000: 
            StructExtensions.read(self.file, "<B")
        if self.version >= 0x9030000: 
            StructExtensions.read(self.file, "<B")
        if self.version >= 0xd010000: 
            StructExtensions.read(self.file, "<f")

class BCDSection_EPL_Char(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        StructExtensions.read(self.file, "<2I")
        Vector3.read(self.file)

class BCDSection_Cam_Chara_move(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)
        Vector3.read(self.file)
        if self.version >= 0x8060100: 
            StructExtensions.read(self.file, "<I")
        StructExtensions.read(self.file, "<f")

class BCDSection_BCDPlay_random(BCDSectionBase):
    def read(self):
        bcdCount = int(StructExtensions.read(self.file, "<I")[0])
        for _ in range(bcdCount):
            NonZeroedString.read(self.file)

class BCDSection_Unit_Helper(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<If")
        if self.version >= 0xd030000: 
            StructExtensions.read(self.file, "<I")
        if self.version >= 0xf020300: 
            StructExtensions.read(self.file, "<I")

class BCDSection_Unit_damage(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2IB")

class BCDSection_EPL_Char_cylinder(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        Vector4.read(self.file)

class BCDSection_Cam_fovy(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<fI")

class BCDSection_Unit_Cylinder(BCDSectionBase):
    def read(self):
        Vector4.read(self.file)

class BCDSection_Cam_rotZ(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<fI")

class BCDSection_Unit_Color(BCDSectionBase):
    def read(self):
        ByteColorRGBA.read(self.file)
        StructExtensions.read(self.file, "<I")

class BCDSection_Unit_Outline(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")

class BCDSection_Env_correct(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<7f")
        if self.version >= 0x9040100: 
            StructExtensions.read(self.file, "<B")

class BCDSection_Env_radialBlur(BCDSectionBase):
    def read(self):
        Vector2.read(self.file)
        Vector2.read(self.file)
        StructExtensions.read(self.file, "<IBI2f")

class BCDSection_Env_straightBlur(BCDSectionBase):
    def read(self):
        Vector2.read(self.file)
        StructExtensions.read(self.file, "<fIfI")

class BCDSection_Env_noiseBlur(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<4Ib2I")

class BCDSection_Env_clearColor(BCDSectionBase):
    def read(self):
        ByteColorRGB.read(self.file)

class BCDSection_Env_DOF(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")
        if self.version >= 0xc010000:
            StructExtensions.read(self.file, "<7f")
        if self.version >= 0xd000100:
            StructExtensions.read(self.file, "<I")

class BCDSection_Unit_rotUnit(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")

class BCDSection_Unit_rotCam(BCDSectionBase):
    def read(self):
        pass

class BCDSection_Env_distortBlur(BCDSectionBase):
    def read(self):
        Vector4.read(self.file)
        StructExtensions.read(self.file, "<I2fI2f")

class BCDSection_Env_monotone(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<3f")

class BCDSection_Env_fill(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<I")
        ByteColorRGBA.read(self.file)
        Vector2.read(self.file)

class BCDSection_Unit_scale(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<f")

class BCDSection_EPL_Char_unit(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        StructExtensions.read(self.file, "<3IfI")

class BCDSection_Env_brightImmediate(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<3B")
        if self.version >= 0x9050000:
            StructExtensions.read(self.file, "<3B")

class BCDSection_Env_saturationImmediate(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<6B")

class BCDSection_Env_hue(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<3B")
        if self.version >= 0x9050000:
            StructExtensions.read(self.file, "<3B")

class BCDSection_Env_hueImmediate(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<6B")

class BCDSection_Fld_HDR_I(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<If")

class BCDSection_Cam_Chara_lookLine(BCDSectionBase):
    def read(self):
        BCDSection_Cam_Chara.read_inner(self.file, self.version)
        StructExtensions.read(self.file, "<2fB")

class BCDSection_Cam_upshot(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_Unit_homeMove(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<fIfB")

class BCDSection_Unit_plane(BCDSectionBase):
    def read(self):
        Vector4.read(self.file)
        if self.version >= 0xf010000:
            StructExtensions.read(self.file, "<I")
        if self.version >= 0xf020000:
            Vector4.read(self.file)
            StructExtensions.read(self.file, "<I")
        if self.version >= 0xf010000:
            StructExtensions.read(self.file, "<If")

class BCDSection_Unit_grayscale(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<B")

class BCDSection_Unit_Face(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<I3f")
        if self.version >= 0x10030400:
            StructExtensions.read(self.file, "<f")

class BCDSection_Unit_AnimEx(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2BfI")
        if self.version >= 0xb020000:
            StructExtensions.read(self.file, "<f")
        StructExtensions.read(self.file, "<I")

class BCDSection_Fld_anim(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<3IfI")

class BCDSection_Fld_objVisible(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<IB")

class BCDSection_Cam_shake(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<I3fI")

class BCDSection_EPL_Stage_helper(BCDSectionBase):
    def read(self):
        BCDSection_EPL_Ex.read_inner(self)
        StructExtensions.read(self.file, "<I")

class BCDSection_EPL_Char_helper(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        StructExtensions.read(self.file, "<2fI")

class BCDSection_padRumble_L(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<4I")

class BCDSection_padRumble_S(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<4I")

class BCDSection_Unit_HelperGoto(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2I")

class BCDSection_Unit_HelperMove(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<IfI")

class BCDSection_Unit_WeaponCulled(BCDSectionBase):
    def read(self):
        pass

class BCDSection_Cam_pan(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2fI")

class BCDSection_EPL_Object_helper(BCDSectionBase):
    def read(self):
        NonZeroedString.read(self.file)
        StructExtensions.read(self.file, "<5f2I")

class BCDSection_Cam_helper(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2I")

class BCDSection_Cam_lookHelper(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<2I")

class BCDSection_Cam_slide(BCDSectionBase):
    def read(self):
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<I")

class BCDSection_Cam_lookHelperLine(BCDSectionBase):
    def read(self):
        StructExtensions.read(self.file, "<7I")

class BCDSection_Fld_objRot(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<2I")

class BCDSection_Fld_colorR(BCDSectionBase_NOTINALPHA3):
    def read(self):
        if self.version >= 0x9050000:
            ByteColorRGBA.read(self.file)
        else:
            ByteColorRGB.read(self.file)

class BCDSection_Mor_setup(BCDSectionBase_NOTINALPHA3):
    def read(self):
        pass

class BCDSection_Mor_pos(BCDSectionBase_NOTINALPHA3):
    def read(self):
        Vector4.read(self.file)

class BCDSection_Mor_goto(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<6f")

class BCDSection_Mor_anim(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<4IHf")

class BCDSection_Mor_path(BCDSectionBase_NOTINALPHA3):
    def read(self):
        NonZeroedString.read(self.file)
        StructExtensions.read(self.file, "<2I")
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<2I")

class BCDSection_Env_ILight(BCDSectionBase_NOTINALPHA3):
    def read(self):
        if self.version >= 0x10010100:
            StructExtensions.read(self.file, "<I")

class BCDSection_Mor_color(BCDSectionBase_NOTINALPHA3):
    def read(self):
        ByteColorRGBA.read(self.file)
        StructExtensions.read(self.file, "<I")

class BCDSection_Unit_CylinderGoto(BCDSectionBase_NOTINALPHA3):
    def read(self):
        Vector4.read(self.file)

class BCDSection_Persona_Setup(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_Persona_Pos(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<f")

class BCDSection_Persona_Anim(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<2I2fB")

class BCDSection_Sound(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_SoundCmn(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_Cam_Chara_lookLineGo(BCDSectionBase_NOTINALPHA3):
    def read(self):
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<3I")
        Vector2.read(self.file)
        StructExtensions.read(self.file, "<B")

class BCDSection_Cam_saveUp(BCDSectionBase_NOTINALPHA3):
    def read(self):
        pass

class BCDSection_Fade(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<2IB")

class BCDSection_SoundSurround(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_Persona_Color(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")
        ByteColorRGBA.read(self.file)
        StructExtensions.read(self.file, "<2I")

class BCDSection_EqPersona_Setup(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")

class BCDSection_EqPersona_Pos(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<IfI2f")

class BCDSection_EqPersona_Anim(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<5I")

class BCDSection_EqPersona_Color(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<I")
        ByteColorRGBA.read(self.file)
        StructExtensions.read(self.file, "<I")
        if self.version >= 0x11030100:
            ByteColorRGBA.read(self.file)

class BCDSection_EPL_Char_Comb(BCDSectionBase_NOTINALPHA3):
    def read(self):
        NonZeroedString.read(self.file)
        Vector3.read(self.file)
        StructExtensions.read(self.file, "<If")

class BCDSection_GUI_damage(BCDSectionBase_NOTINALPHA3):
    def read(self):
        StructExtensions.read(self.file, "<2If")

class BCDSection_Cam_crossfade(BCDSectionBase_NOTINALPHA3):
    def read(self):
        pass

class BCDSectionFactory:
    def create(file : io.BufferedReader, version):
        # sectionID, Field24, StartTime, Duration, EventAreaID
        header = StructExtensions.read(file, "<2I2fB")
        match header[0]:
            case 0:
                return BCDSection_BCDPlay(file, header, version)
            case 1:
                return BCDSection_Unit_Anim(file, header, version)
            case 2:
                return BCDSection_EPL(file, header, version)
            case 3:
                return BCDSection_EPL_Coordinate(file, header, version)
            case 4:
                return BCDSection_Unit_crdSet(file, header, version)
            case 5:
                return BCDSection_Unit_move(file, header, version)
            case 6:
                return BCDSection_Unit_rot(file, header, version)
            case 7:
                return BCDSection_Unit_rotPos(file, header, version)
            case 8:
                return BCDSection_Unit_homePos(file, header, version)
            case 9:
                return BCDSection_Cam(file, header, version)
            case 10:
                return BCDSection_Unit_Culled(file, header, version)
            case 11:
                return BCDSection_Cam_overview(file, header, version)
            case 12:
                return BCDSection_EPL_Ex(file, header, version)
            case 13:
                return BCDSection_Env_bright(file, header, version)
            case 14:
                return BCDSection_Fld_color(file, header, version)
            case 15:
                return BCDSection_Fld_HDR(file, header, version)
            case 16:
                return BCDSection_Env_saturation(file, header, version)
            case 17:
                return BCDSection_Unit_DyingCulled(file, header, version)
            case 18:
                return BCDSection_Cam_chant(file, header, version)
            case 19:
                return BCDSection_Cam_move(file, header, version)
            case 20:
                return BCDSection_Cam_goto(file, header, version)
            case 21:
                return BCDSection_Cam_Chara(file, header, version)
            case 22:
                return BCDSection_Cam_Chara_goto(file, header, version)
            case 23:
                return BCDSection_Cam_Chara_fixed(file, header, version)
            case 24:
                return BCDSection_Cam_Chara_look(file, header, version)
            case 25:
                return BCDSection_Cam_Chara_view(file, header, version)
            case 26:
                return BCDSection_Unit_pathMove(file, header, version)
            case 27:
                return BCDSection_EPL_Char(file, header, version)
            case 28:
                return BCDSection_Cam_Chara_move(file, header, version)
            case 29:
                return BCDSection_BCDPlay_random(file, header, version)
            case 30:
                return BCDSection_Unit_Helper(file, header, version)
            case 31:
                return BCDSection_Unit_damage(file, header, version)
            case 32:
                return BCDSection_EPL_Char_cylinder(file, header, version)
            case 33:
                return BCDSection_Cam_fovy(file, header, version)
            case 34:
                return BCDSection_Unit_Cylinder(file, header, version)
            case 35:
                return BCDSection_Cam_rotZ(file, header, version)
            case 36:
                return BCDSection_Unit_Color(file, header, version)
            case 37:
                return BCDSection_Unit_Outline(file, header, version)
            case 38:
                return BCDSection_Env_correct(file, header, version)
            case 39:
                return BCDSection_Env_radialBlur(file, header, version)
            case 40:
                return BCDSection_Env_straightBlur(file, header, version)
            case 41:
                return BCDSection_Env_noiseBlur(file, header, version)
            case 42:
                return BCDSection_Env_clearColor(file, header, version)
            case 43:
                return BCDSection_Env_DOF(file, header, version)
            case 44:
                return BCDSection_Unit_rotUnit(file, header, version)
            case 45:
                return BCDSection_Unit_rotCam(file, header, version)
            case 46:
                return BCDSection_Env_distortBlur(file, header, version)
            case 47:
                return BCDSection_Env_monotone(file, header, version)
            case 48:
                return BCDSection_Env_fill(file, header, version)
            case 49:
                return BCDSection_Unit_scale(file, header, version)
            case 50:
                return BCDSection_EPL_Char_unit(file, header, version)
            case 51:
                return BCDSection_Env_brightImmediate(file, header, version)
            case 52:
                return BCDSection_Env_saturationImmediate(file, header, version)
            case 53:
                return BCDSection_Env_hue(file, header, version)
            case 54:
                return BCDSection_Env_hueImmediate(file, header, version)
            case 55:
                return BCDSection_Fld_HDR_I(file, header, version)
            case 56:
                return BCDSection_Cam_Chara_lookLine(file, header, version)
            case 57:
                return BCDSection_Cam_upshot(file, header, version)
            case 58:
                return BCDSection_Unit_homeMove(file, header, version)
            case 59:
                return BCDSection_Unit_plane(file, header, version)
            case 60:
                return BCDSection_Unit_grayscale(file, header, version)
            case 61:
                return BCDSection_Unit_Face(file, header, version)
            case 62:
                return BCDSection_Unit_AnimEx(file, header, version)
            case 63:
                return BCDSection_Fld_anim(file, header, version)
            case 64:
                return BCDSection_Fld_objVisible(file, header, version)
            case 65:
                return BCDSection_Cam_shake(file, header, version)
            case 66:
                return BCDSection_EPL_Stage_helper(file, header, version)
            case 67:
                return BCDSection_EPL_Char_helper(file, header, version)
            case 68:
                return BCDSection_padRumble_L(file, header, version)
            case 69:
                return BCDSection_padRumble_S(file, header, version)
            case 70:
                return BCDSection_Unit_HelperGoto(file, header, version)
            case 71:
                return BCDSection_Unit_HelperMove(file, header, version)
            case 72:
                return BCDSection_Unit_WeaponCulled(file, header, version)
            case 73:
                return BCDSection_Cam_pan(file, header, version)
            case 74:
                return BCDSection_Fld_objRot(file, header, version)
            case 75:
                return BCDSection_EPL_Object_helper(file, header, version)
            case 76:
                return BCDSection_Cam_helper(file, header, version)
            case 77:
                return BCDSection_Cam_lookHelper(file, header, version)
            case 78:
                return BCDSection_Cam_slide(file, header, version)
            case 79:
                return BCDSection_Cam_lookHelperLine(file, header, version)
            case 80:
                return BCDSection_Fld_colorR(file, header, version)
            case 81:
                return BCDSection_Mor_setup(file, header, version)
            case 82:
                return BCDSection_Mor_pos(file, header, version)
            case 83:
                return BCDSection_Mor_goto(file, header, version)
            case 84:
                return BCDSection_Mor_anim(file, header, version)
            case 85:
                return BCDSection_Mor_path(file, header, version)
            case 86:
                return BCDSection_Env_ILight(file, header, version)
            case 87:
                return BCDSection_Mor_color(file, header, version)
            case 88:
                return BCDSection_Unit_CylinderGoto(file, header, version)
            case 89:
                return BCDSection_Persona_Setup(file, header, version)
            case 90:
                return BCDSection_Persona_Pos(file, header, version)
            case 91:
                return BCDSection_Persona_Anim(file, header, version)
            case 92:
                return BCDSection_Sound(file, header, version)
            case 93:
                return BCDSection_SoundCmn(file, header, version)
            case 94:
                return BCDSection_Cam_Chara_lookLineGo(file, header, version)
            case 95:
                return BCDSection_Cam_saveUp(file, header, version)
            case 96:
                return BCDSection_Fade(file, header, version)
            case 97:
                return BCDSection_SoundSurround(file, header, version)
            case 98:
                return BCDSection_Persona_Color(file, header, version)
            case 99:
                return BCDSection_EqPersona_Setup(file, header, version)
            case 100:
                return BCDSection_EqPersona_Pos(file, header, version)
            case 101:
                return BCDSection_EqPersona_Anim(file, header, version)
            case 102:
                return BCDSection_EqPersona_Color(file, header, version)
            case 103:
                return BCDSection_EPL_Char_Comb(file, header, version)
            case 104:
                return BCDSection_GUI_damage(file, header, version)
            case 105:
                return BCDSection_Cam_crossfade(file, header, version)
            case _:
                raise Exception("Unknown BCD type " + str(header[0]) + " @ " + str(hex(file.tell())))

def open_file(filename):
    file = open(filename, "rb")

    header = struct.unpack("<2I", file.read(0x8))
    print("File " + filename + " :")
    print("version " + str(hex(header[0])) + ", " + str(header[1]) + " sections")

    section_count = 0
    out_file_data = bytearray()
    for _ in range(header[1]):
        start = file.tell()
        curr = BCDSectionFactory.create(file, header[0])
        curr.read()
        size = file.tell() - start
        if curr.is_valid():
            file.seek(-size, 1)
            out_file_data += file.read(size)
            section_count += 1
        print("Section " + str(curr.header[0]) + ": @ " + str(hex(start) + ": " + str(curr.is_valid())))
    new_header = struct.pack("<2I", header[0], section_count)
    out_file_data = new_header + out_file_data
    # print(out_file_data)

def main():
    if len(sys.argv) < 2:
        print("Error: Missing filename")
        return
    path = os.path.abspath(sys.argv[1])
    if os.path.isdir(path):
        for file in [
            os.path.join(parts[0], file) 
            for parts in os.walk(path) if len(parts[2]) != 0 
            for file in parts[2] if file.lower().endswith(".bcd")
            ]:
            open_file(file)

    elif os.path.isfile(path):
        open_file(path)

if __name__ == "__main__":
    main()