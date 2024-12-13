import flet as ft
import threading
from chat_program.chat_client_class import *
from parser import *
import datetime


def chat_view(page: ft.Page, client: Client):
    page.title = "Tonpy"
    page.update()

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
        controls=page.session.get("chat_history"),
    )

    def send_message_click(e):
        if new_message.value != "":
            chat.controls.append(
                ChatMessageSent(new_message.value, page.session.get("usrname"))
            )
            client.read_input(new_message.value)
        new_message.value = ""
        new_message.focus()
        page.update()

    def list_users(e):
        client.read_input("who")

    def logout(e):
        client.read_input("q")
        page.go("/login")

    def time(e):
        time = ft.AlertDialog(
            title=ft.Text("Time"),
            content=ft.Text(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            actions=[ft.TextButton("Cancel", on_click=lambda _: page.close(time))],
        )
        page.overlay.append(time)
        time.open = True
        page.update()

    def submit_poem(number):
        poem_dialog.open = False  # 关闭对话框
        page.update()  # 刷新页面
        client.read_input(f"p{number}")

    def poem(e):
        text_field = ft.TextField(hint_text="Enter the chapter")

        global poem_dialog  # 声明为全局变量，以便在其他函数中访问
        poem_dialog = ft.AlertDialog(
            title=ft.Text("Get your poem!"),
            content=text_field,
            actions=[
                ft.TextButton(
                    text="Get it", on_click=lambda e: submit_poem(text_field.value)
                )
            ],
        )
        page.dialog = poem_dialog  # 将对话框添加到页面
        poem_dialog.open = True  # 打开对话框
        page.update()  # 刷新页面

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    def game_click(e):
        page.overlay.append(game_choose)
        game_choose.open = True
        page.update()

    def gomoku_choose(e):
        client.read_input("gomoku_invite")
        page.close(game_choose)

    game_choose = ft.AlertDialog(
        title=ft.Text("Game center"),
        content=ft.Column(
            controls=[
                ft.TextButton("gomoku", on_click=gomoku_choose),
                ft.TextButton(
                    "Something else", on_click=lambda _: page.close(game_choose)
                ),
            ]
        ),
        actions=[ft.TextButton("Cancel", on_click=lambda _: page.close(game_choose))],
    )

    # Add everything to the page
    return ft.View(
        route="/chat",
        appbar=ft.AppBar(
            title=ft.Text(f"Tonpy"),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                tooltip="Logout",
                on_click=logout,
            ),
        ),
        controls=[
            ft.Container(
                content=chat,
                # border=ft.border.all(1, ft.Colors.OUTLINE),
                # border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "List users",
                        icon=ft.Icons.PEOPLE_ROUNDED,
                        tooltip="Find out who else is here",
                        on_click=list_users,
                    ),
                    # ft.FilledButton(
                    #     "Logout",
                    #     icon=ft.Icons.LOGOUT_ROUNDED,
                    #     bgcolor="red",
                    #     on_click=logout,
                    # ),
                    ft.FilledButton(
                        "Time",
                        icon=ft.Icons.ACCESS_TIME,
                        on_click=time,
                    ),
                    ft.FilledButton(
                        "Poem",
                        icon=ft.Icons.BOOK,
                        on_click=poem,
                    ),
                ]
            ),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.VIDEOGAME_ASSET,
                        tooltip="Game",
                        on_click=game_click,
                    ),
                    new_message,
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=send_message_click,
                    ),
                ]
            ),
        ],
    )
