from alpha3_utils import *
import io

class MsgHeader:
    def stream_read(file: io.BufferedReader):
        header = StructExtensions.read(file, "<2BH6I2BH")

class MsgDialogHeader:
    def stream_read(file: io.BufferedReader):
        parts = StructExtensions.read(file, "2I")
        ret = file.tell()
        file.seek(parts[2], 0)
        file.seek(ret, 0)