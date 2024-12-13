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
            grpList = ft.ListView(
                expand=True,
                spacing=10,
                auto_scroll=True,
            )
            self = page.session.get("usrname")
            for idx, users in msg["results"]["users"].items():
                if users == 0 and idx != self:
                    usrList.controls.append(
                        ft.OutlinedButton(
                            text=idx,
                            on_click=lambda e: output("c " + e.control.text),
                            width=300,
                        )
                    )
            for idx, users in msg["results"]["groups"].items():
                grpList.controls.append(
                    ft.OutlinedButton(
                        text="Group: " + ", ".join(users),
                        on_click=lambda e: output(
                            "c " + e.control.text[7:].split(", ")[0]
                        ),
                        width=300,
                    )
                )

            if len(usrList.controls) or len(grpList.controls):
                return ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("System", weight="bold"),
                            ft.Text("Please select the user/group to connect"),
                            usrList,
                            grpList,
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

            def submit_choice(e):
                page.close(invitation)
                if e.control.text == "Yes":
                    output("y")
                else:
                    output("n")

            invitation = ft.AlertDialog(
                title=ft.Text(msg["game"] + " request from " + msg["from"]),
                actions=[
                    ft.TextButton(text="Yes", on_click=submit_choice),
                    ft.TextButton(text="No", on_click=submit_choice),
                ],
            )
            page.open(invitation)
            return ft.Column()
        else:
            return ChatMessageReceive(json.dumps(msg))
    else:
        return ChatMessageReceive(msg)
