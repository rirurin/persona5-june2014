from alpha3_utils import *
import io
import sys

class MsgHeader:
    def __init__(self, data, size):
        self.data = data
        self.size = size

    def stream_read(file: io.BufferedReader):
        data = StructExtensions.read(file, ">2BH6I2BH")
        return MsgHeader(data, file.tell())

    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">2BH6I2BH", *self.data))
    
class MsgToken:
    def stream_read(file: io.BufferedReader):
        raise Exception("called base class")
    def stream_write(self, file: io.BytesIO):
        raise Exception("called base class")
    def print_token(self):
        raise Exception("called base class")
    
class MsgTextToken(MsgToken):
    def __init__(self, text):
        self.text = text
    def stream_read(file: io.BufferedReader):
        chars = bytearray()
        curr, = StructExtensions.read(file, "B")
        while curr != 0x0 and curr != 0xa:
            chars += struct.pack("B", curr)
            curr, = StructExtensions.read(file, "B")
        return MsgTextToken(bytes(chars))
    def stream_write(self, file: io.BytesIO):
        file.write(self.text)
        file.write(struct.pack("B", 0xa))
    def print_token(self):
        print(self.text)

class MsgFuncToken(MsgToken):
    def __init__(self, table_idx, func_idx, params):
        self.table_idx = table_idx
        self.func_idx = func_idx
        self.params = params
    def stream_read(file: io.BufferedReader):
        func_header, = StructExtensions.read(file, ">H")
        table_idx = (func_header >> 0x5) & 7
        func_idx = func_header & 0x1f
        func_size = (func_header & 0xf00) >> 7
        params = []
        if func_size > 2:
            params = StructExtensions.read(file, ">" + "H" * int((func_size - 2) / 2))
        return MsgFuncToken(table_idx, func_idx, params)
    def print_token(self):
        print("[f " + str(self.table_idx) + " " + str(self.func_idx) + "]")

class MsgDialog:
    def __init__(self, pages, speaker_id, tokens):
        self.pages = pages
        self.speaker_id = speaker_id
        self.tokens = tokens
    def stream_read(file: io.BufferedReader, base: int):
        parts = StructExtensions.read(file, ">2I")
        ret = file.tell()
        file.seek(base + parts[1], 0)
        name = str(file.read(24), "ASCII", errors="ignore")
        print(name)
        speaker_info = StructExtensions.read(file, ">2H")
        page_start_offsets = StructExtensions.read(file, ">" + ("I" * speaker_info[0]))
        # token_size, = StructExtensions.read(file, ">I")
        _, = StructExtensions.read(file, ">I")
        tokens: list[MsgToken] = []
        for o in page_start_offsets:
            file.seek(base + o, 0)
            curr_token, = StructExtensions.read(file, "B")
            file.seek(-1, 1)
            while curr_token != 0:
                if curr_token & 0xf0 == 0xf0:
                    print(hex(file.tell()))
                    fn_token: MsgToken = MsgFuncToken.stream_read(file)
                    fn_token.print_token()
                    tokens.append(fn_token)
                elif curr_token != 0xa:
                    tx_token: MsgToken = MsgTextToken.stream_read(file)
                    tx_token.print_token()
                    tokens.append(tx_token)
                curr_token, = StructExtensions.read(file, "B")
                file.seek(-1, 1)
        file.seek(ret, 0)
        return MsgDialog(speaker_info[0], speaker_info[1], tokens)

class MsgSpeaker:
    def __init__(self, header):
        self.header = header
    def stream_read(file: io.BufferedReader):
        parts = StructExtensions.read(file, ">2IL")
        return MsgSpeaker(parts)
    def stream_write(self, file: io.BytesIO):
        file.write(struct.pack(">2IL", *self.header))

class MsgFile:
    header: MsgHeader
    dialogs: list[MsgDialog]
    speaker: MsgSpeaker
    def __init__(self, header, dialogs, speaker):
        self.header = header
        self.dialogs = dialogs
        self.speaker = speaker
    def stream_read(file: io.BufferedReader):
        header = MsgHeader.stream_read(file)
        dialog_count = header.data[8]
        print("dialog count: " + str())
        dialogs = []
        for _ in range(dialog_count):
            dialogs.append(MsgDialog.stream_read(file, header.size))
        speaker = MsgSpeaker.stream_read(file)
        return MsgFile(header, dialogs, speaker)

def main():
    # make sure directory is PS3_GAME/USRDIR
    if len(sys.argv) < 2:
        print("Missing location")
        return
    file = open(sys.argv[1], "rb")
    MsgFile.stream_read(file)
    
if __name__ == "__main__":
    main()