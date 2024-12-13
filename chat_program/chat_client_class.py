import time
import socket
import select
import sys
import json
import flet as ft
from chat_program.chat_utils import *
import chat_program.client_state_machine as csm
from parser import *


class Client:
    def __init__(self, args):
        self.peer = ""
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ""
        self.local_msg = ""
        self.peer_msg = ""
        self.args = args
        self.exception = ""
        self.board = [[0] * 15 for _ in range(15)]

    def init_board(self):
        self.board = [[0] * 15 for _ in range(15)]

    def place_stone(self, x, y, player_id):
        self.board[x][y] = player_id

    def get_stone(self, x, y):
        if 0 <= x < 15 and 0 <= y < 15:
            return self.board[x][y]
        return -1

    def check_winner(self, x, y, player_id):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                if self.get_stone(x + dx * i, y + dy * i) == player_id:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                if self.get_stone(x - dx * i, y - dy * i) == player_id:
                    count += 1
                else:
                    break
            if count >= 5:
                winner = "You" if player_id == 1 else "Opponent"
                self.system_msg += f"{winner} win!\n"
                dialog = ft.AlertDialog(
                    title=ft.Text(f"Game Over! {winner} wins!"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: self.page.go("/chat"))
                    ],
                    on_dismiss=lambda e: self.page.go("/chat"),
                )
                self.page.open(dialog)
                self.page.update()
                return True
        return False

    def update_gomoku_move(self, x, y, player="peer"):
        # 我方一直是红，对方一直是蓝
        color = "red" if player == "me" else "blue"
        grid = self.page.views[-1].controls[-1]
        cell = grid.controls[x * 15 + y]
        cell.content = ft.Container(
            width=20,
            height=20,
            bgcolor=color,
            border_radius=10,
        )
        self.page.update()

    def quit(self):
        self.page.session.set("chat_history", None)
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = (self.args, CHAT_PORT) if self.args else SERVER
        try:
            self.socket.connect(svr)
            self.sm = csm.ClientSM(self.socket, self)
            self.exception = ""
        except Exception as e:
            self.exception = e

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ""
        peer_msg = []
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            try:
                msg = json.loads(self.system_msg)
                self.page.views[-1].controls[0].content.controls.append(
                    parse(msg, output=self.read_input, page=self.page)
                )
            except:
                if len(self.page.views[-1].controls) > 0:
                    self.page.views[-1].controls[0].content.controls.append(
                        parse(self.system_msg)
                    )
                    self.page.session.set(
                        "chat_history", self.page.views[-1].controls[0].content.controls
                    )
            self.page.update()
            self.system_msg = ""

    def read_input(self, text):
        self.console_input.append(text)

    def print_instructions(self):
        self.system_msg += menu

    def change_list_users(page):
        # 找到目标控件
        for control in page.views[-1].controls:
            if isinstance(control, ft.Row):  # 如果是包含按钮的 Row
                for sub_control in control.controls:
                    if (
                        isinstance(sub_control, ft.FilledButton)
                        and sub_control.text == "List users"
                    ):
                        # 修改按钮的文本和点击事件
                        sub_control.text = "List groups"
        page.update()

    def run_chat(self, page):
        self.page = page
        self.system_msg += "Welcome to ICS chat\n"
        self.system_msg += "Please enter your name: "
        self.output()

        while self.login() != True:
            self.output()
        self.system_msg += "Welcome, " + self.get_name() + "!"
        self.output()

        while self.sm.get_state() != S_OFFLINE:

            my_msg, peer_msg = self.get_msgs()
            if my_msg or peer_msg:
                self.system_msg += self.sm.proc(my_msg, peer_msg)
                self.output()
                if self.sm.get_state() == S_GOMOKU_START:
                    page.go("/gomoku")
                if self.sm.get_state() == S_GAMING_GOMOKU_YOUR_TURN:
                    self.page.views[-1].controls[1] = ft.Text(
                        "Your turn", weight="bold"
                    )
                if self.sm.get_state() == S_GAMING_GOMOKU_PEER_TURN:
                    self.page.views[-1].controls[1] = ft.Text(
                        "Peer turn", weight="bold"
                    )
                self.page.update()
            time.sleep(CHAT_WAIT)

        self.quit()

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action": "login", "name": self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == "ok":
                self.state = S_LOGGEDIN

                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return True
            elif response["status"] == "duplicate":
                self.system_msg += "Duplicate username, try again"
                return False
        else:
            return False
