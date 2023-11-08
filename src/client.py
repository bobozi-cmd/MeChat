from socket import socket, AF_INET, SOCK_DGRAM


class MeChatClient():

    def __init__(self, host: str, port: int) -> None:
        self.addr = (host, port)
        self._client = None
        self.name = ""

    def register(self, name: str):
        self._client = socket(AF_INET, SOCK_DGRAM)
        self._client.settimeout(10)
        self.name = name
        self._client.sendto(f"register: {name}".encode('utf-8'), self.addr)
        
        # wait for response or failed
        try:
            resp = self._client.recvfrom(4096)[0].decode('utf-8')
        except TimeoutError as e:
            print("MeChat Server disconnect!")
            exit(-1)

        resp_toks = resp.split(':')
        if resp_toks[0].strip() != 'register':
            print(f"Error Response: {resp}")
            exit(-1)
        if resp_toks[1].strip() != 'ok':
            print(f"Failed to Connect to server: {resp}")
            exit(-1)

    def run(self):
        if self._client == None:
            print("Not register to Server!")
            exit(-1)

        while True:
            msg = input("client>")
            self._client.sendto(f"message: {msg}".encode('utf-8'), self.addr)
            
            try:
                resp = self._client.recvfrom(4096)[0].decode('utf-8')
            except TimeoutError:
                print("MeChat Server disconnect!")
                exit(-1)
                
            print(f'server:{resp}')

