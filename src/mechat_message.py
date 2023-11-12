from enum import IntEnum
from dataclasses import dataclass
import datetime, logging


logging.basicConfig(
    filename=f'mechat_{datetime.datetime.today().strftime("%Y_%m_%d")}.log',
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
)

class MeMessageType(IntEnum):
    REGISTER = 0
    MESSAGE = 1
    ERROR = 2


@dataclass
class MeMessage:
    msg_type: MeMessageType
    msg: str
    ctime: datetime.time = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

    def __repr__(self) -> str:
        return self.msg

    @classmethod
    def serialize(cls, msg: "MeMessage") -> bytes:
        assert type(msg) == MeMessage
        return f"{msg.msg_type} {msg.ctime} {msg}".encode("utf-8")

    @classmethod
    def deserialize(cls, msg_b: bytes) -> "MeMessage":
        """
        >>> msg1 = MeMessage(MeMessageType.REGISTER, "bobo zhou")
        >>> msg2 = MeMessage.deserialize(MeMessage.serialize(msg1))
        >>> msg1.msg_type == msg2.msg_type
        True
        >>> msg1.msg == msg2.msg
        True
        >>> msg1.ctime == msg2.ctime
        True
        """
        msg = msg_b.decode("utf-8")
        toks = msg.split(" ")
        logging.debug(f"{toks}")
        if len(toks) >= 3:
            return MeMessage(
                msg_type=MeMessageType(int(toks[0])), msg=" ".join(toks[2:]), ctime=toks[1]
            )
        else:
            return MeMessage(
                msg_type=MeMessageType.ERROR, msg=f"deserialize failed, recieve msg is {toks}"
            )
