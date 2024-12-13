import json
from chat_program.chat_utils import *
from parser import *


class ClientSM:
    def __init__(self, s, client):
        self.state = S_OFFLINE
        self.peer = ""
        self.me = ""
        self.out_msg = ""
        self.s = s
        self.client = client  # 引用客户端对象，用于更新UI等

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += "You are connected with " + self.peer + "\n"
            return True
        elif response["status"] == "busy":
            self.out_msg += "User is busy. Please try again later\n"
        elif response["status"] == "self":
            self.out_msg += "Cannot talk to yourself (sick)\n"
        else:
            self.out_msg += "User is not online, try again later\n"
        return False

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += "You are disconnected from " + self.peer + "\n"
        self.peer = ""

    def proc(self, my_msg, peer_msg):
        self.out_msg = ""

        # 先处理peer_msg，及时更新UI
        if len(peer_msg) > 0:
            pm = json.loads(peer_msg)
            if pm.get("action") == "gomoku_move":
                # 根据from判断是谁落子
                from_player = pm["from"]
                x = pm["coord"]["x"]
                y = pm["coord"]["y"]
                player_id = 1 if from_player == self.me else 2

                # 更新棋盘UI
                self.client.place_stone(x, y, player_id)
                self.client.update_gomoku_move(
                    x, y, "me" if from_player == self.me else "peer"
                )

                # 检查胜负
                if self.client.check_winner(x, y, player_id):
                    # 如果产生胜者,可根据需要设置状态为S_LOGGEDIN或S_OFFLINE，以结束游戏
                    # self.state = S_LOGGEDIN
                    pass
                else:
                    # 根据落子方决定状态切换
                    if from_player == self.me:
                        # 如果是自己下的子，已经在发出move时切过一次状态为S_GAMING_GOMOKU_PEER_TURN
                        # 因此这里不需要切换状态。
                        pass
                    else:
                        # 对手下子到达，现在轮到自己下子
                        self.state = S_GAMING_GOMOKU_YOUR_TURN

            elif pm.get("action") == "connect":
                if pm.get("status") == "request":
                    self.peer = pm["from"]
                    self.out_msg += "Request from " + self.peer + "\n"
                    self.out_msg += "You are connected with " + self.peer
                    self.out_msg += ". Chat away!\n\n"
                    self.out_msg += "------------------------------------\n"
                    self.state = S_CHATTING
            elif pm.get("action") == "exchange":
                self.out_msg += pm["from"] + pm["message"]
            elif pm.get("action") == "disconnect":
                self.state = S_LOGGEDIN
            elif pm.get("action") == "game_invite":
                self.out_msg += pm["game"] + " invite from " + pm["from"] + "\n"
                self.out_msg += "Type 'y' to accept, anything else to decline\n"
                self.state = S_GAME_DECIDING
            elif pm.get("action") == "game_response":
                if pm["response"] == "y":
                    self.state = S_GOMOKU_START
                else:
                    self.out_msg += f"{pm['game']} game declined\n"
                    self.state = S_CHATTING
            elif pm.get("action") == "game_start":
                self.client.init_board()
                if pm["turn"] == "you":
                    self.state = S_GAMING_GOMOKU_YOUR_TURN
                else:
                    self.state = S_GAMING_GOMOKU_PEER_TURN
            # 其它消息类型继续保持原样

        # 根据当前状态处理my_msg
        if self.state == S_LOGGEDIN:
            if len(my_msg) > 0:
                if my_msg == "q":
                    self.state = S_OFFLINE
                elif my_msg == "time":
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in
                elif my_msg == "who":
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Here are all the users in the system:\n"
                    self.out_msg += logged_in
                elif my_msg == "gomoku_invite":
                    self.out_msg += "You need someone to play with"
                elif my_msg.startswith("c"):
                    peer = my_msg[1:].strip()
                    if self.connect_to(peer):
                        self.state = S_CHATTING
                        self.out_msg += "Connect to " + peer + ". Chat away!\n\n"
                        self.out_msg += "-----------------------------------\n"
                    else:
                        self.out_msg += "Connection unsuccessful\n"
                elif my_msg.startswith("?"):
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if len(search_rslt) > 0:
                        self.out_msg += search_rslt + "\n"
                    else:
                        self.out_msg += f"'{term}' not found\n"
                elif my_msg.startswith("p") and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if len(poem) > 0:
                        self.out_msg += poem + "\n\n"
                    else:
                        self.out_msg += f"Sonnet {poem_idx} not found\n\n"
                else:
                    self.out_msg += menu

        elif self.state == S_CHATTING:
            if len(my_msg) > 0:
                if my_msg == "bye":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ""
                elif my_msg == "gomoku_invite":
                    mysend(
                        self.s, json.dumps({"action": "game_invite", "game": "gomoku"})
                    )
                    self.out_msg += "gomoku invite sent"
                    self.state = S_GAME_INVITING
                else:
                    mysend(
                        self.s,
                        json.dumps(
                            {
                                "action": "exchange",
                                "from": "[" + self.me + "]",
                                "message": my_msg,
                            }
                        ),
                    )

            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state == S_GAME_INVITING:
            # game_response已在peer_msg处理
            pass

        elif self.state == S_GAME_DECIDING:
            if len(my_msg) > 0:
                if my_msg == "y":
                    mysend(
                        self.s,
                        json.dumps(
                            {
                                "action": "game_response",
                                "game": "gomoku",
                                "response": "y",
                                "invitation_from": self.peer,
                            }
                        ),
                    )
                    self.state = S_GOMOKU_START
                else:
                    mysend(
                        self.s,
                        json.dumps(
                            {
                                "action": "game_response",
                                "game": "gomoku",
                                "response": "decline",
                            }
                        ),
                    )
                    self.out_msg += "gomoku game declined\n"
                    self.state = S_CHATTING

        elif self.state == S_GOMOKU_START:
            # game_start已在peer_msg中处理
            pass

        elif self.state == S_GAMING_GOMOKU_YOUR_TURN:
            if my_msg.startswith("gomoku_move"):
                coord = json.loads(my_msg[12:])
                # 不在此更新UI，等待服务器返回gomoku_move
                # 只发送消息给服务器
                mysend(self.s, json.dumps({"action": "gomoku_move", "coord": coord}))
                # 先假设已落子，但UI更新等服务器消息
                self.state = S_GAMING_GOMOKU_PEER_TURN

        elif self.state == S_GAMING_GOMOKU_PEER_TURN:
            # 对手落子已在peer_msg处理
            pass

        else:
            self.out_msg += "How did you wind up here??\n"
            print_state(self.state)

        return self.out_msg
