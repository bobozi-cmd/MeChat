from socket import socket, AF_INET, SOCK_DGRAM


class MeChatServer():

    def __init__(self, host: str, port: int) -> None:
        self.addr = (host, port)
        self._server = None
        self.users: dict[str, tuple[str, int]] = {}

    def find_name(self, address: tuple) -> str:
        for name, addr in self.users.items():
            if addr == address:
                return name
        return ""

    def register_client(self, name: str, addr: tuple):
        if name in self.users:
            msg = "Name has been occupied"
            self._server.sendto(f"register: {msg}".encode('utf-8'), addr)
        else:
            self.users[name] = addr
            msg = "ok"
            self._server.sendto(f"register: {msg}".encode('utf-8'), addr)

    def run(self):
        self._server = socket(AF_INET, SOCK_DGRAM)
        self._server.bind(self.addr)
        
        while True:
            msg, addr = self._server.recvfrom(4096)
            tag, content = msg.decode('utf-8').split(':')
            if tag == 'register':
                self.register_client(content, addr)
            elif tag == 'message':
                print(f"{self.find_name(addr)}:{content}")
            self._server.sendto("next".encode('utf-8'), addr)

