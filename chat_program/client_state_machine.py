import random
from chat_program.chat_utils import *
import json
from parser import *
import flet as ft


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ""
        self.me = ""
        self.out_msg = ""
        self.s = s

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
        # ==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        # ==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == "q":
                    # self.out_msg += "See you next time!\n"
                    self.state = S_OFFLINE

                elif my_msg == "time":
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == "who":
                    mysend(self.s, json.dumps({"action": "list"}))
                    # logged_in = json.loads(myrecv(self.s))["results"]
                    # self.out_msg += "Here are all the users in the system:\n"
                    # self.out_msg += logged_in
                    self.out_msg += myrecv(self.s)

                elif my_msg == "gomoku_invite":
                    self.out_msg += "You need someone to play with"

                elif my_msg[0] == "c":
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += "Connect to " + peer + ". Chat away!\n\n"
                        self.out_msg += "-----------------------------------\n"
                    else:
                        self.out_msg += "Connection unsuccessful\n"

                elif my_msg[0] == "?":
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + "\n"
                    else:
                        self.out_msg += "'" + term + "'" + " not found\n"

                elif my_msg[0] == "p" and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if len(poem) > 0:
                        self.out_msg += poem + "\n\n"
                    else:
                        self.out_msg += "Sonnet " + poem_idx + " not found\n\n"

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += "Request from " + self.peer + "\n"
                    self.out_msg += "You are connected with " + self.peer
                    self.out_msg += ". Chat away!\n\n"
                    self.out_msg += "------------------------------------\n"
                    self.state = S_CHATTING

        # ==============================================================================
        # Start chatting, 'bye' for quit
        # This is event handling instate "S_CHATTING"
        # ==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:  # my stuff going out
                if my_msg == "bye":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ""
                elif my_msg == "gomoku_invite":
                    mysend(
                        self.s,
                        json.dumps({"action": "game_invite", "game": "gomoku"}),
                    )
                    # response = json.loads(myrecv(self.s))
                    # if response["status"] == "success":
                    #     print("sucess1!!!!!!")
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
            if len(peer_msg) > 0:  # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "game_invite":
                    self.out_msg += (
                        peer_msg["game"] + "invite from " + peer_msg["from"] + "\n"
                    )
                    self.out_msg += "Type 'y' to y, anything else to decline\n"
                    # TODO should have a GUI dialog box
                    self.state = S_GAME_DECIDING
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        # ==============================================================================
        # invalid state
        # ==============================================================================
        elif self.state == S_GAME_INVITING:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["response"] == "y":
                    # self.out_msg += f"{peer_msg["game"]} game starting\n"
                    self.state = S_GOMOKU_START
                if peer_msg["response"] == "decline":
                    self.out_msg += f"{peer_msg["game"]} game declined\n"
                    self.state = S_CHATTING
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
                                # TODO self.peer should be the actual person who send the invite
                                # TODO chat_server is now handling the "from_name"
                            }
                        ),
                    )
                    # self.out_msg += f"Game starting\n"
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
                            # TODO target should be different by game
                        ),
                    )
                    self.out_msg += "gomoku game declined\n"
                    self.state = S_CHATTING
        elif self.state == S_GOMOKU_START:
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "game_start":
                    if peer_msg["turn"] == "you":
                        self.state = S_GAMING_GOMOKU_YOUR_TURN
                    if peer_msg["turn"] == "peer":
                        self.state = S_GAMING_GOMOKU_PEER_TURN
        elif self.state == S_GAMING_GOMOKU_YOUR_TURN:
            if my_msg.startswith("gomoku_move"):
                print(my_msg)
                coord = json.loads(my_msg[12:])
                mysend(self.s, json.dumps({"action": "gomoku_move", "coord": coord}))
        elif self.state == S_GAMING_GOMOKU_PEER_TURN:
            if len(peer_msg) > 0:
                self.out_msg += peer_msg
        else:
            self.out_msg += "How did you wind up here??\n"
            print_state(self.state)

        return self.out_msg
