class MsgProtocol:

    def __init__(self, chat_commands: list, encoder: str = 'utf-8', bytesize: int = 1024):
        self.chat_command_map: dict = {command: i for i, command in enumerate(chat_commands)}
        self.encoder = encoder
        self.bytesize = bytesize


    def encode(self, msg: str) -> bytes:

        if msg in self.chat_command_map:
            encoded_msg = self.chat_command_map[msg].to_bytes(1, byteorder='big')
            return encoded_msg
        encoded_msg = (0).to_bytes(1, byteorder='big')
        
        try:
            msg_length = len(msg)
            msg_byte_length = msg_length.to_bytes(4, byteorder='big')
            encoded_msg += msg_byte_length
        except OverflowError:
            print('message is too big')

        encoded_msg += msg.encode(self.encoder)      
        
        return encoded_msg
    

    def decode_command(self, command_id: bytes) -> str:
        command_id = int.from_bytes(command_id, byteorder='big')
        for key, val in self.chat_command_map:
            if val == command_id:
                return key
    

    def decode_length(self, length: bytes) -> int:
        length = int.from_bytes(length, bytetsize='big')
        return length


    def decode_msg(self, msg: bytes) -> str:
        return msg.decode(self.encoder)
