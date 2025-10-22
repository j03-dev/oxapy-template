from oxapy import HttpServer

from app.api import auth, user
from app.core.config import ADDR

server = HttpServer(ADDR)
server.attach(auth.router)
server.attach(user.router)


def main():
    server.run()


if __name__ == "__main__":
    main()
