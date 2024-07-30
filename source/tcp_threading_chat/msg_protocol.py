from enum import Enum
from typing import NamedTuple


class Call(NamedTuple):
    call: str
    id: int

class Calls(Enum):
    MSG = Call()
    INFO = Call('info', 1)
    MEMBERS = Call('members', 2)
    ALL_CHAT = Call('all', 3)
    DIRECT_MESSAGES = Call('')



class MsgProtocol:



    @staticmethod
    def encode(msg: str):


        return msg
    
    @staticmethod
    def decode(msg: str):

        return msg
