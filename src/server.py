from socket import socket, AF_INET, SOCK_DGRAM

from message import MeMsgType, MeMessage, pack_msg, unpack_msg

class MeChatServer():

    def __init__(self, host: str, port: int) -> None:
        self.addr = (host, port)
        self._server = None
        self.users: dict[str, tuple[str, int]] = {}
        self.chat_group = {}

    def find_name(self, address: tuple) -> str:
        for name, addr in self.users.items():
            if addr == address:
                return name
        return ""

    def register_client(self, name: str, addr: tuple):
        if name in self.users:
            msg = MeMessage(MeMsgType.REGISTER, "Name has been occupied")
        else:
            self.users[name] = addr
            msg = MeMessage(MeMsgType.REGISTER, "ok")
        self._server.sendto(pack_msg(msg), addr)        
        
    def select_client(self, user_to: str, addr: tuple):
        if user_to == "":
            msg = MeMessage(MeMsgType.SELECT, f"{list(self.users.keys())}")
        else:
            msg = MeMessage(MeMsgType.SELECT, "ok")

            user_from = self.find_name(addr)
            self.chat_group[user_to] = user_from
            self.chat_group[user_from] = user_to
            # every client need a thread for send and a thread for recieve
            msg2 = MeMessage(MeMsgType.MESSAGE, f"{user_from} select you to talk with")
            self._server.sendto(pack_msg(msg2), self.users[user_to])
        
        self._server.sendto(pack_msg(msg), addr)
        

    def run(self):
        self._server = socket(AF_INET, SOCK_DGRAM)
        self._server.bind(self.addr)
        
        while True:
            msg_b, addr = self._server.recvfrom(4096)
            me_msg: MeMessage = unpack_msg(msg_b)
            if me_msg.msg_type == MeMsgType.REGISTER:
                self.register_client(me_msg.msg, addr)
            elif me_msg.msg_type == MeMsgType.SELECT:
                self.select_client(me_msg.msg, addr)
            elif me_msg.msg_type == MeMsgType.MESSAGE:
                user_from = self.find_name(addr)
                if user_from in self.chat_group:
                    user_to = self.chat_group[user_from]
                    msg = MeMessage(MeMsgType.MESSAGE, f"{user_from} : {me_msg}")
                    self._server.sendto(pack_msg(msg), self.users[user_to])
                else:
                    msg = MeMessage(MeMsgType.MESSAGE, "next")
                    self._server.sendto(pack_msg(msg), addr)
