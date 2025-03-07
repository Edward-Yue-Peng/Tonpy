import random
import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp


class Server:
    def __init__(self):
        self.new_clients = []
        self.logged_name2sock = {}
        self.logged_sock2name = {}
        self.all_sockets = []
        self.group = grp.Group()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        self.indices = {}
        self.sonnet = indexer.PIndex("AllSonnets.txt")

    def new_client(self, sock):
        print("new client...")
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        try:
            msg = json.loads(myrecv(sock))
            print("login:", msg)
            if len(msg) > 0 and msg["action"] == "login":
                name = msg["name"]
                if not self.group.is_member(name):
                    self.new_clients.remove(sock)
                    self.logged_name2sock[name] = sock
                    self.logged_sock2name[sock] = name
                    if name not in self.indices.keys():
                        try:
                            self.indices[name] = pkl.load(open(name + ".idx", "rb"))
                        except IOError:
                            self.indices[name] = indexer.Index(name)
                    print(name + " logged in")
                    self.group.join(name)
                    mysend(sock, json.dumps({"action": "login", "status": "ok"}))
                else:
                    mysend(sock, json.dumps({"action": "login", "status": "duplicate"}))
                    print(name + " duplicate login attempt")
            else:
                self.logout(sock)
        except:
            if sock in self.all_sockets:
                self.all_sockets.remove(sock)

    def logout(self, sock):
        if sock not in self.logged_sock2name:
            return
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + ".idx", "wb"))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        if sock in self.all_sockets:
            self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

    def handle_msg(self, from_sock):
        msg = myrecv(from_sock)
        if len(msg) > 0:
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    rmsg = json.dumps({"action": "connect", "status": "self"})
                    mysend(from_sock, rmsg)
                elif self.group.is_member(to_name):
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    rmsg = json.dumps({"action": "connect", "status": "success"})
                    mysend(from_sock, rmsg)
                    # 通知对方有请求
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(
                            to_sock,
                            json.dumps(
                                {
                                    "action": "connect",
                                    "status": "request",
                                    "from": from_name,
                                }
                            ),
                        )
                else:
                    rmsg = json.dumps({"action": "connect", "status": "no-user"})
                    mysend(from_sock, rmsg)

            elif msg["action"] == "game_invite":
                game = msg["game"]
                from_name = self.logged_sock2name[from_sock]
                to_name = self.group.list_me(from_name)[1]
                to_sock = self.logged_name2sock[to_name]
                mysend(
                    to_sock,
                    json.dumps(
                        {"action": "game_invite", "game": game, "from": from_name}
                    ),
                )

            elif msg["action"] == "game_response":
                from_name = self.logged_sock2name[from_sock]
                to_name = self.group.list_me(from_name)[1]
                to_sock = self.logged_name2sock[to_name]
                mysend(
                    to_sock,
                    json.dumps(
                        {
                            "action": "game_response",
                            "game": msg["game"],
                            "response": msg["response"],
                            "from": from_name,
                        }
                    ),
                )
                if msg["response"] == "y":
                    if random.choice([True, False]):
                        mysend(
                            from_sock,
                            json.dumps(
                                {
                                    "action": "game_start",
                                    "game": "gomoku",
                                    "turn": "you",
                                }
                            ),
                        )
                        mysend(
                            to_sock,
                            json.dumps(
                                {
                                    "action": "game_start",
                                    "game": "gomoku",
                                    "turn": "peer",
                                }
                            ),
                        )
                    else:
                        mysend(
                            from_sock,
                            json.dumps(
                                {
                                    "action": "game_start",
                                    "game": "gomoku",
                                    "turn": "peer",
                                }
                            ),
                        )
                        mysend(
                            to_sock,
                            json.dumps(
                                {
                                    "action": "game_start",
                                    "game": "gomoku",
                                    "turn": "you",
                                }
                            ),
                        )

            elif msg["action"] == "gomoku_wait":
                pass

            elif msg["action"] == "gomoku_move":
                from_name = self.logged_sock2name[from_sock]
                msg["from"] = from_name
                the_guys = self.group.list_me(from_name)
                # 广播给对战中的所有玩家
                for g in the_guys:
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps(msg))

            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                said2 = text_proc(msg["message"], from_name)
                self.indices[from_name].add_msg_and_index(said2)
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)
                    mysend(
                        to_sock,
                        json.dumps(
                            {
                                "action": "exchange",
                                "from": msg["from"],
                                "message": msg["message"],
                            }
                        ),
                    )

            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                rmsg = self.group.list_all()
                mysend(from_sock, json.dumps({"action": "list", "results": rmsg}))

            elif msg["action"] == "poem":
                poem_indx = int(msg["target"])
                from_name = self.logged_sock2name[from_sock]
                poem = self.sonnet.get_poem(poem_indx)
                poem = "\n".join(poem).strip()
                mysend(from_sock, json.dumps({"action": "poem", "results": poem}))

            elif msg["action"] == "time":
                ctime = time.strftime("%d.%m.%y,%H:%M", time.localtime())
                mysend(from_sock, json.dumps({"action": "time", "results": ctime}))

            elif msg["action"] == "search":
                term = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                search_rslt = "\n".join(
                    [x[-1] for x in self.indices[from_name].search(term)]
                )
                mysend(
                    from_sock, json.dumps({"action": "search", "results": search_rslt})
                )

            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps({"action": "disconnect"}))

        else:
            # client died unexpectedly
            self.logout(from_sock)

    def run(self):
        print("starting server...")
        while True:
            read, write, error = select.select(self.all_sockets, [], [])
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            if self.server in read:
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


main()
