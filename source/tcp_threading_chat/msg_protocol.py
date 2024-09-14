import struct

class MsgProtocol:
    #0 stands for non command messages
    chat_commands_map = {
        '\\quit' : 1,  # disconnect
        '\\members' : 2,  #list of members
        '\\info' : 3,  #list of commands
        '\\all' : 4  #switch to allchat
    }


    def __init__(self):
        self.encoder: str = 'utf-8'
        self.bytesize: int = 1024
        self.max_length: int = 2048


    def encode(self, msg: str) -> bytes:
        return msg.encode(self.encoder)


    def pack(self, msg: str) -> bytes:
        length = len(self.encode(msg))
        if length > self.max_length:
            print('msg is too big')
            return None
        command_id = 0
        if msg.lower() in MsgProtocol.chat_commands_map:
            command_id = MsgProtocol.chat_commands_map[msg]
            try:
                return struct.pack('!BI', command_id, length)
            except Exception as e:
                print(f'Error {e} while packing command_id')

        try:
            return struct.pack('!BI', command_id, length) + self.encode(msg)
        except Exception as e:
            print(f'Error {e} while packing')
            return None
        

    def unpack(self, msg: bytes) -> tuple:
        try:
            command_id, msg_length = struct.unpack('!BI', msg)
            return command_id, msg_length
        except Exception as e:
            print(f'Error {e} while unpacking')
            return None


    def decode_command(self, command_id: int) -> str:
        for key, val in MsgProtocol.chat_commands_map.items():
            if val == command_id:
                return key
        raise ValueError
    

    def decode(self, msg: bytes) -> str:
        return msg.decode(self.encoder)