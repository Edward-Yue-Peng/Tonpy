import flet as ft
import threading
from chat_program.chat_client_class import *
from parser import *
import datetime
from chat_ai import chatai


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
            actions=[ft.TextButton("OK", on_click=lambda _: page.close(time))],
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
        page.dialog = poem_dialog
        poem_dialog.open = True
        page.update()

    def submit_ai(question):
        ai_dialog.open = False
        page.update()
        chat.controls.append(ChatMessageReceive(chatai(question), "QWEN AI"))
        page.update()

    def ai_click(e):
        text_field = ft.TextField()

        global ai_dialog
        ai_dialog = ft.AlertDialog(
            title=ft.Text("Ask AI"),
            content=text_field,
            actions=[
                ft.TextButton(
                    text="Get it", on_click=lambda e: submit_ai(text_field.value)
                )
            ],
        )
        page.dialog = ai_dialog
        ai_dialog.open = True
        page.update()

    def submit_search(number):
        search_dialog.open = False
        page.update()
        client.read_input(f"? {number}")

    def search_click(e):
        text_field = ft.TextField(on_submit=lambda e: submit_search(text_field.value))
        global search_dialog
        search_dialog = ft.AlertDialog(
            title=ft.Text("Search your words"),
            content=text_field,
            actions=[
                ft.TextButton(
                    text="submit", on_click=lambda e: submit_search(text_field.value)
                )
            ],
        )
        page.dialog = search_dialog
        search_dialog.open = True
        page.update()

    def leave_click(e):
        client.read_input(f"bye")

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
        # page.overlay.append(game_choose)
        # game_choose.open = True
        page.open(game_choose)
        page.update()

    def gomoku_choose(e):
        client.read_input("gomoku_invite")
        page.close(game_choose)

    game_choose = ft.AlertDialog(
        title=ft.Text("Invite to play a game?"),
        actions=[
            ft.TextButton("Yes", on_click=gomoku_choose),
            ft.TextButton("Cancel", on_click=lambda _: page.close(game_choose)),
        ],
    )
    list_users_botton = ft.OutlinedButton(
        "List",
        icon=ft.Icons.PEOPLE_ROUNDED,
        tooltip="Find out available users/groups",
        on_click=list_users,
    )
    # Add everything to the page
    return ft.View(
        route="/chat",
        appbar=ft.AppBar(
            title=ft.Text(f"Tonpy"),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS,
                tooltip="Logout",
                on_click=logout,
            ),
            center_title=True,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.MANAGE_SEARCH,
                    tooltip="Search",
                    on_click=search_click,
                ),
            ],
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
                    list_users_botton,
                    ft.IconButton(
                        icon_size=20,
                        icon=ft.Icons.ACCESS_TIME,
                        on_click=time,
                    ),
                    ft.IconButton(
                        icon_size=20,
                        icon=ft.Icons.BOOK,
                        on_click=poem,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EXIT_TO_APP_ROUNDED,
                        icon_size=20,
                        tooltip="Leave the group",
                        on_click=leave_click,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.COMPUTER,
                        icon_size=20,
                        tooltip="Ask AI",
                        on_click=ai_click,
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
