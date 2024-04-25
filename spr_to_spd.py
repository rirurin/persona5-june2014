import os
import sys
import struct

def main():
    if len(sys.argv) < 2:
        print("Error: Missing filename")
        return
    filename = os.path.basename(sys.argv[1])
    filesize = os.stat(sys.argv[1]).st_size
    file = open(sys.argv[1], "rb")
    print("reading " + filename + " (" + str(filesize) +  " bytes) ")

    header = struct.unpack("<2H4I2H2I", file.read(0x20))
    print(str(header[6]) + " textures, " + str(header[7]) + " sprites")

    tex_offset = 0x20 + header[6] * 0x30 + header[7] * 0xa0 

    fileout_name = os.path.splitext(sys.argv[1])[0] + "_out.spd"
    fileout = open(fileout_name, "wb")

    # write output header
    fileout.write(b"SPR0")
    fileout.write((2).to_bytes(4, "little"))
    fileout.write(bytes(8)) # filesize, field0c
    fileout.write((0x20).to_bytes(4, "little"))
    fileout.write(header[6].to_bytes(2, "little"))
    fileout.write(header[7].to_bytes(2, "little"))
    fileout.write((0x20).to_bytes(4, "little"))
    fileout.write((0x20 + header[6] * 0x30).to_bytes(4, "little"))

    pTextures = []
    pSprites = []
    # read texture and sprite pointers
    for _ in range(header[6]):
        pTextures.append(struct.unpack("<2I", file.read(0x8)))
    for _ in range(header[7]):
        pSprites.append(struct.unpack("<2I", file.read(0x8)))
    # read texture contents
    for tex in pTextures:
        file.seek(tex[1])
        texData = struct.unpack("<2HI", file.read(0x8))
        # print(texData[2])
        file.seek(0x1c, 1) # jump to name field in TMX header
        text_buf = file.read(0x10)
        tex_name = text_buf.decode("utf-8").split("\0")[0]
        tex_target_path = os.path.join(os.path.dirname(sys.argv[1]), (tex_name + ".dds"))
        tex_size = os.stat(tex_target_path).st_size
        tex_dds = open(tex_target_path, "rb") # find dds of same name
        # write texture out
        fileout.write((pTextures.index(tex) + 1).to_bytes(4, "little"))
        fileout.write(bytes(0x4))
        fileout.write(tex_offset.to_bytes(4, "little"))
        # write dds file
        prev_pos = fileout.tell()
        fileout.seek(tex_offset)
        fileout.write(tex_dds.read())
        tex_dds.seek(0)
        fileout.seek(prev_pos)
        tex_offset += tex_size
        fileout.write(tex_size.to_bytes(4, "little"))
        # read dds header to get width and height
        tex_dds.seek(0xc)
        tex_dimension = struct.unpack("<2I", tex_dds.read(8))
        fileout.write(tex_dimension[1].to_bytes(4, "little"))
        fileout.write(tex_dimension[0].to_bytes(4, "little"))
        fileout.write(bytes(0x8))
        fileout.write(text_buf)
    # read sprite contents
    for spr in pSprites:
        file.seek(spr[1])
        file.seek(0x4, 1)
        # p5 encoding is used, treat it as an opaque block
        spr_name = file.read(0x10)
        spr_data = struct.unpack("<24I2H2I", file.read(0x6c))
        spr_pos = (spr_data[16],spr_data[17],spr_data[18],spr_data[19])
        spr_color = (spr_data[20],spr_data[21],spr_data[22],spr_data[23])
        # write sprite out
        fileout.write((pSprites.index(spr) + 1).to_bytes(4, "little"))
        fileout.write(spr_data[0].to_bytes(4, "little"))
        fileout.write(spr_data[1].to_bytes(4, "little"))
        fileout.write(bytes(0x14))
        fileout.write(spr_pos[0].to_bytes(4, "little")) # top left
        fileout.write(spr_pos[1].to_bytes(4, "little"))
        fileout.write(spr_pos[2].to_bytes(4, "little")) # bottom right
        fileout.write(spr_pos[3].to_bytes(4, "little"))
        fileout.write(bytes(0x8))
        fileout.write(spr_pos[2].to_bytes(4, "little")) # scale
        fileout.write(spr_pos[3].to_bytes(4, "little"))
        fileout.write(bytes(0x10))
        fileout.write(spr_color[0].to_bytes(4, "little")) # color
        fileout.write(spr_color[1].to_bytes(4, "little"))
        fileout.write(spr_color[2].to_bytes(4, "little"))
        fileout.write(spr_color[3].to_bytes(4, "little"))
        fileout.write(bytes(0x10))
        fileout.write(spr_name)
        fileout.write(bytes(0x20))
    fileout.seek(0, 2)
    file_size_out = fileout.tell()
    fileout.seek(0x8)
    fileout.write(file_size_out.to_bytes(4, "little"))

if __name__ == "__main__":
    main()