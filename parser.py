import flet as ft
import json
from chat_program.chat_utils import *


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessageSent(ft.Row):

    def __init__(self, message: Message, usrname):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        single_message = ft.Column(
            [
                ft.Text(usrname, weight="bold"),
                ft.Text(message, selectable=True),
            ],
            tight=True,
            spacing=5,
        )
        self.controls = [
            ft.Container(
                content=single_message,
                alignment=ft.alignment.center_right,
                expand=True,
            )
        ]


class ChatMessageReceive(ft.Row):
    def __init__(self, message: Message, usrname="System"):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START

        single_message = ft.Column(
            [
                ft.Text(usrname, weight="bold"),
                ft.Text(message, selectable=True),
            ],
            tight=True,
            spacing=5,
        )
        self.controls = [
            ft.Container(
                content=single_message,
                expand=True,
            )
        ]


class FletEvent:
    def __init__(self, control):
        self.control = control


def parse(msg, page=None, output=None):
    if type(msg) == dict:
        if msg["action"] == "list":
            usrList = ft.ListView(
                expand=True,
                spacing=10,
                auto_scroll=True,
            )
            self = page.session.get("usrname")
            for user, status in msg["results"]["users"].items():
                if status == 0 and user != self:
                    usrList.controls.append(
                        ft.OutlinedButton(
                            text=user,
                            on_click=lambda e: output("c " + e.control.text),
                            width=300,
                        )
                    )
            if len(usrList.controls):
                return ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("System", weight="bold"),
                            ft.Text("Please select the users to connect"),
                            usrList,
                        ],
                        tight=True,
                        spacing=5,
                    ),
                    alignment=ft.alignment.center_right,
                    expand=True,
                )
            else:
                return ChatMessageReceive("No available users.")
        elif msg["action"] == "exchange":
            return ChatMessageReceive(msg["message"], msg["from"])
        elif msg["action"] == "game_invite":
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text("System", weight="bold"),
                        ft.Text(msg["game"] + " request from " + msg["from"]),
                    ],
                    tight=True,
                    spacing=5,
                ),
                alignment=ft.alignment.center_right,
                expand=True,
            )
        else:
            return ChatMessageReceive(json.dumps(msg))
    else:
        return ChatMessageReceive(msg)
