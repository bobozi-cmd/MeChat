import socket, threading, queue, logging, datetime, sys
from traceback import print_tb

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


gloabl_user_list = {}
gloabl_msg_queue = queue.Queue()  # thread-safe
global_user_lock = threading.Lock()

msg_limit = 1024
max_client = 5


class MeChatServer(threading.Thread):
    def __init__(
        self,
        addr: _Address,
        users_list: dict[str, tuple[socket.socket, _Address]] = gloabl_user_list,
        users_lock: threading.Lock = global_user_lock,
        msg_queue: queue.Queue = gloabl_msg_queue,
    ):
        threading.Thread.__init__(self)
        self.addr = addr
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users_list = users_list
        self.users_lock = users_lock
        self.msg_queue = msg_queue

    def find_user(self, conn: socket.socket | _Address) -> str | None:
        temp_table = self.users_list.items()
        idx = 0 if type(conn) == socket.socket else 1
        
        for usr, connection in temp_table:
            if connection[idx] == conn:
                return usr
        return None

    def register_user(self, username: str, conn: socket.socket, addr: _Address) -> int:
        with self.users_lock:
            if username not in self.users_list:
                self.users_list[username] = (conn, addr)
                logging.info(f"{username} become a new user!")
            else:
                logging.error(f"{username} has exist!")
                return -1
        return 0

    def unregister_user(self, username: str):
        with self.users_lock:
            self.users_list.pop(username, None)
        logging.info(f"{username} exited!\n{self.users_list}")

    def unregister_user_by_conn(self, conn: socket.socket | _Address):
        target = None
        logging.info(f"{conn} exited!\n")
        with self.users_lock:
            target = self.find_user(conn)

        if target:
            self.unregister_user(target)

    def do_register(self, msg: MeMessage, conn: socket.socket, addr: _Address):
        username = None
        assert msg.msg_type == MeMessageType.REGISTER
        assert self.register_user(msg.msg, conn, addr) == 0

        username = msg.msg
        ret_msg = MeMessage(
            MeMessageType.REGISTER, "system >\n OK!"
        )
        conn.send(MeMessage.serialize(ret_msg))
        # welcome_msg = MeMessage(
        #     MeMessageType.MESSAGE, f"system >\n Welcome {username}!"
        # )
        # self.broadcast("system", MeMessage.serialize(welcome_msg))
        return username

    def show_online_user(self) -> list[str]:
        ol_users = []
        with self.users_lock:
            ol_users = list(self.users_list.keys())
        return ol_users

    def broadcast(self, username: str, msg_b: bytes):
        with self.users_lock:
            for _, connection in self.users_list.items():
                try:
                    connection[0].send(msg_b)
                except:
                    pass

    def send_service(self):
        while True:
            if not self.msg_queue.empty():
                username, msg_b = self.msg_queue.get()  # (username, msg)
                self.broadcast(username, msg_b)

    def receive_service(self, conn: socket.socket, addr: _Address):
        username = None
        while True:
            try:
                msg_b = conn.recv(msg_limit)
                msg = MeMessage.deserialize(msg_b)
                assert msg.msg_type != MeMessageType.ERROR

                logging.debug(f"[{username}] : {msg}")
                if username == None:
                    # User must register firstly
                    username = self.do_register(msg, conn, addr)
                else:
                    owner_msg = MeMessage(
                        msg.msg_type, f"{username} >\n {msg}", msg.ctime
                    )
                    self.msg_queue.put((username, MeMessage.serialize(owner_msg)))
            except:
                ttype, tvalue, ttraceback = sys.exc_info()
                print_tb(ttraceback)
                self.unregister_user_by_conn(addr)
                conn.close()
                exit(-1)

    def run(self):
        self._server.bind(self.addr)
        self._server.listen(max_client)
        send_thr = threading.Thread(target=self.send_service)
        send_thr.start()

        while True:
            conn, addr = self._server.accept()
            logging.info(f"Client {addr} is connecting...")
            t = threading.Thread(target=self.receive_service, args=(conn, addr))
            t.start()

        self._server.close()


if __name__ == "__main__":
    import argparse

    server_p = argparse.ArgumentParser()
    server_p.add_argument(
        "-H", "--host", help="Server host address", required=True, type=str
    )
    server_p.add_argument(
        "-P", "--port", help="Server port number", default=18889, type=int
    )

    args = server_p.parse_args()

    mechat_server = MeChatServer((args.host, args.port))
    mechat_server.start()
