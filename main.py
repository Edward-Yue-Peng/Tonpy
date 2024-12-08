import flet as ft
from chat_program.chat_client_class import *


def main(page: ft.Page):
    page.title = "Tonpy"
    page.update()

    server_addr = ft.TextField(label="Enter server address")
    client = Client(server_addr.value)

    def init(e):
        page.close(ask_addr)
        client.run_chat(page)

    ask_addr = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Enter server address"),
        content=ft.Column([server_addr], tight=True),
        actions=[ft.ElevatedButton(text="OK", on_click=init)],
        actions_alignment="end",
    )

    page.open(ask_addr)

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
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.Icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                ),
            ]
        ),
    )


ft.app(main)
