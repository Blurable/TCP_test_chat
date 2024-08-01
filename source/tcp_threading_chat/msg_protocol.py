from enum import Enum
from typing import NamedTuple
import re


class Call(NamedTuple):
    text: str
    id: int

class Calls(Enum):
    MSG = Call(r'.*', 0)
    INFO = Call('\\info', 1)
    MEMBERS = Call('\\members', 2)
    ALL_CHAT = Call('\\all', 3)
    DIRECT_MESSAGES = Call(r'\\[a-zA-Z]+', 4)



class MsgProtocol:



    @staticmethod
    def encode(msg: str):
        encoded_msg = ''
        match msg:
            case Calls.INFO.value.text:
                encoded_msg += Calls.INFO.value.id
            case Calls.MEMBERS.value.text:
                encoded_msg += Calls.MEMBERS.value.id
            case Calls.ALL_CHAT.value.text:
                encoded_msg += Calls.ALL_CHAT.value.id
            case msg if re.match(Calls.DIRECT_MESSAGES.value.text, msg):
                encoded_msg += Calls.DIRECT_MESSAGES.value.id
            case Calls.INFO.value.text:
                encoded_msg += Calls.INFO.value.id
            case Calls.INFO.value.text:
                encoded_msg += Calls.INFO.value.id
        
        return msg
    
    @staticmethod
    def decode(msg: str):

        return msg
