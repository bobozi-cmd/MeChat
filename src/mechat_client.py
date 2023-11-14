import socket, threading, logging, datetime, sys, signal

from mechat_message import *

from typing import Any
from typing_extensions import TypeAlias

_Address: TypeAlias = tuple[Any, ...] | str | Any

logging.basicConfig(
    filename=f'mechat_{datetime.datetime.today().strftime("%Y_%m_%d")}.log',
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
)

msg_limit = 1024

def handler(signum: "signal._SIGNUM", frame):
    if signal.SIGINT == signum:
        exit(0)

class MeChatClient():

    def __init__(self, server_addr: _Address, username: str) -> None:
        self.server_addr = server_addr
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username

    def send_msg(self, msg: MeMessage):
        try:
            self._client.send(MeMessage.serialize(msg))
        except:
            logging.error(f"Connection met error!")
            exit(-1)

    def do_register(self):
        registered = False

        msg = MeMessage(MeMessageType.REGISTER, self.username)
        self.send_msg(msg)

        while not registered:
            msg_b = self._client.recv(msg_limit)
            msg = MeMessage.deserialize(msg_b)
            if msg.msg_type == MeMessageType.REGISTER:
                # if msg.msg == 'system >\n OK!':
                registered = True
            elif msg.msg_type == MeMessageType.ERROR:
                print(f"{msg.ctime} {msg}")
                self._client.close()
                exit(-1)
        print(f"Register Successed!")

    def do_send(self):
        while True:
            try:
                msg_info = input(">")
                if msg_info.strip() != '':
                    msg = MeMessage(MeMessageType.MESSAGE, msg_info)
                    self.send_msg(msg)
            except:
                print("do_send met error!")
                break
    
    def do_recv(self):
        while True:
            try:
                # self._client.setblocking(False)
                msg_b = self._client.recv(msg_limit)
                if msg_b:
                    msg = MeMessage.deserialize(msg_b)
                    if msg.msg_type == MeMessageType.MESSAGE:
                        print(f"{msg.ctime} {msg}")
                    elif msg.msg_type == MeMessageType.ERROR:
                        print(f"{msg.ctime} {msg}")
            except:
                print("do_recv bye~")
                self._client.close()
                break

    def run(self):
        self._client.connect(self.server_addr)
        self.do_register()
        
        recv_thr = threading.Thread(target=self.do_recv)
        recv_thr.start()
        
        self.do_send()
        self._client.close()
        recv_thr.join()

if __name__ == "__main__":
    import argparse

    client_p = argparse.ArgumentParser()
    client_p.add_argument(
        "-H", "--host", help="Client host address", required=True, type=str
    )
    client_p.add_argument(
        "-P", "--port", help="Client port number", default=18889, type=int
    )
    client_p.add_argument(
        "-N", "--name", help="Client name", required=True, type=str
    )

    args = client_p.parse_args()

    # signal.signal(signal.SIGINT, handler=handler)

    mechat_server = MeChatClient((args.host, args.port), args.name)
    mechat_server.run()

        