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
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        single_message = ft.Column(
            [
                ft.Text("System", weight="bold"),
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


def parse(msg, output=None):
    if type(msg) == dict:
        if msg["action"] == "list":
            usrList = ft.ListView(
                expand=True,
                spacing=10,
                auto_scroll=True,
            )

            for user, status in msg["results"]["users"].items():
                if status == 0:
                    usrList.controls.append(
                        ft.OutlinedButton(
                            text=user, on_click=lambda _: output("c " + user), width=300
                        )
                    )
            return usrList
        else:
            return ChatMessageReceive(json.dumps(msg))
    else:
        return ChatMessageReceive(msg)
