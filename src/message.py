import pickle, datetime
from enum import IntEnum
from dataclasses import dataclass


class MeMsgType(IntEnum):
    REGISTER = 0  # register user  
    SELECT   = 1  # select user to talk
    MESSAGE  = 2  # message for talking


@dataclass
class MeMessage():
    msg_type : MeMsgType
    msg      : str
    ctime    : datetime.time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    def __repr__(self) -> str:
        return f"{self.ctime} >\n{self.msg}"


def pack_msg(msg: MeMessage) -> bytes:
    assert type(msg) == MeMessage
    # TODO: encrypt msg
    return pickle.dumps(msg)


def unpack_msg(msg_b: bytes) -> MeMessage:
    # TODO: decrypt msg
    msg = pickle.loads(msg_b)
    assert type(msg) == MeMessage
    return msg



if __name__ == "__main__":
    msg = MeMessage(MeMsgType.REGISTER, "Hello")
    print(msg)

    msg_b = pack_msg(msg)
    print("pack :", msg_b)
    print("unpack :", unpack_msg(msg_b))
