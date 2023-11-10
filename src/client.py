from socket import socket, AF_INET, SOCK_DGRAM

from message import MeMsgType, MeMessage, pack_msg, unpack_msg

class MeChatClient():

    def __init__(self, host: str, port: int) -> None:
        self.addr = (host, port)
        self._client = None
        self.name = ""

    def register(self, name: str):
        self._client = socket(AF_INET, SOCK_DGRAM)
        self._client.settimeout(10)
        self.name = name
        msg = MeMessage(MeMsgType.REGISTER, f"{name}")
        self._client.sendto(pack_msg(msg), self.addr)
        
        # wait for response or failed
        try:
            resp: MeMessage = unpack_msg(self._client.recvfrom(4096)[0])
        except TimeoutError as e:
            print("MeChat Server disconnect!")
            exit(-1)

        assert resp.msg_type == MeMsgType.REGISTER
        assert resp.msg == 'ok'

        print("Register Success!")

    def select_talkmate(self):
        msg = MeMessage(MeMsgType.SELECT, "")
        self._client.sendto(pack_msg(msg), self.addr)
        try:
            resp: MeMessage = unpack_msg(self._client.recvfrom(4096)[0])
        except TimeoutError as e:
            print("MeChat Server disconnect!")
            exit(-1)

        assert resp.msg_type == MeMsgType.SELECT

        users: list = eval(resp.msg)
        users.remove(self.name)
        
        while True:
            print(f"Please select the user to talk:")
            for i, user in enumerate(users):
                print(f"({i}) {user}")
            idx = input("Please input the number of user:")
            if idx.isdigit() and int(idx) >= 0 and int(idx) < len(users):
                break
        msg = MeMessage(MeMsgType.SELECT, f"{users[int(idx)]}")
        self._client.sendto(pack_msg(msg), self.addr)
        try:
            resp: MeMessage = unpack_msg(self._client.recvfrom(4096)[0])
        except TimeoutError as e:
            print("MeChat Server disconnect!")
            exit(-1)
        
        assert resp.msg_type == MeMsgType.SELECT
        assert resp.msg == 'ok'

        print("Select Success!")


    def run(self):
        if self._client == None:
            print("Not register to Server!")
            exit(-1)

        while True:
            msg_content = input("client>")
            msg = MeMessage(MeMsgType.MESSAGE, msg_content)
            self._client.sendto(pack_msg(msg), self.addr)
            
            try:
                resp: MeMessage = unpack_msg(self._client.recvfrom(4096)[0])
            except TimeoutError:
                print("MeChat Server disconnect!")
                exit(-1)
                
            print(f'{resp.msg}')

