import flet as ft
import threading
from chat_program.chat_client_class import *


def chat_view(page: ft.Page, client):
    page.title = "Tonpy"
    page.update()

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    def send_message_click(e):
        if new_message.value != "":
            chat.controls.append(ft.Text(new_message.value))
            client.read_input(new_message.value)
        new_message.value = ""
        new_message.focus()
        page.update()

    def game_click(e):
        page.go("/game")
        pass

    def list_users(e):
        client.read_input("who")

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

    # Add everything to the page
    return ft.View(
        route="/chat",
        controls=[
            ft.Container(
                content=chat,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    ft.FilledButton(
                        "list users",
                        icon=ft.Icons.PEOPLE_ROUNDED,
                        tooltip="Find out who else is here",
                        on_click=list_users,
                    )
                ]
            ),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.VIDEOGAME_ASSET,
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
