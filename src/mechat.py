import argparse, signal, logging, datetime

from client import MeChatClient
from server import MeChatServer


logging.basicConfig(
    filename=f'mechat_{datetime.datetime.today().strftime("%Y_%m_%d")}.log',
    level=logging.DEBUG,
    format="[%(asctime)s] - [%(levelname)s] - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d-%H:%M:%S",
)


def handler(signum: "signal._SIGNUM", frame):
    if signal.SIGINT == signum:
        exit(0)


def run_server(args):
    mechat_server = MeChatServer(args.host, args.port)
    mechat_server.run()


def run_client(args):
    mechat_client = MeChatClient(args.host, args.port)
    mechat_client.register(args.name)
    if args.state == "pos":
        mechat_client.select_talkmate()
    mechat_client.run()


def main():

    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="type", required=True)
    
    server_p = subp.add_parser("server", help="Start a server")
    server_p.add_argument("-H", "--host", help="Server host address", required=True, type=str)
    server_p.add_argument("-P", "--port", help="Server port number", default=18888, type=int)

    client_p = subp.add_parser("client", help="Start a client")
    client_p.add_argument("-H", "--host", help="Client host address", required=True, type=str)
    client_p.add_argument("-P", "--port", help="Client port number", default=18888, type=int)
    client_p.add_argument("-N", "--name", help="Client Name", type=str, default=f'cli_{int(datetime.datetime.today().timestamp())}')
    client_p.add_argument("-S", "--state", help="Client State", type=str, required=True)

    args = parser.parse_args()

    signal.signal(signal.SIGINT, handler=handler)

    logging.debug(f"mechat args: {args}")

    if args.type == "server":
        run_server(args)
    else:
        run_client(args)


if __name__ == "__main__":
    main()
