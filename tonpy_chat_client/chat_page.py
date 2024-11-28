import flet as ft
from qwen import chat_qwen


class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessageSent(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        single_message = ft.Column(
            [
                ft.Text(message.user_name, weight="bold"),
                ft.Text(message.text, selectable=True),
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
                ft.Text(message.user_name, weight="bold"),
                ft.Text(message.text, selectable=True),
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


def chat_page_view(page: ft.Page):
    route_parts = page.route.split("/")
    if len(route_parts) > 2:
        selected_user = route_parts[2]
    else:
        selected_user = "Unknown"

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            new_message_copy = new_message.value
            new_message.value = ""
            new_message.focus()
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message_copy,
                    message_type="sent_message",
                )
            )
            page.pubsub.send_all(
                Message(
                    selected_user,
                    chat_qwen(str(new_message_copy)),
                    message_type="received_message",
                )
            )
            page.update()

    def on_message(message: Message):
        if message.message_type == "sent_message":
            m = ChatMessageSent(message)
        elif message.message_type == "received_message":
            m = ChatMessageReceive(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    join_user_name = ft.TextField(
        label="Enter your name to join the chat",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    chat = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True,
    )

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

    sending_area = ft.Row(
        [
            ft.IconButton(
                icon=ft.icons.ADD,
                tooltip="More",
            ),
            new_message,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=send_message_click,
            ),
        ]
    )
    return ft.View(
        route=f"/chat/{selected_user}",
        appbar=ft.AppBar(
            title=ft.Text(f"Chat with {selected_user}"),
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                tooltip="Back to User List",
                on_click=lambda _: page.go("/users"),
            ),
        ),
        controls=[
            ft.Container(
                content=chat,
                padding=10,
                expand=True,
            ),
            sending_area,
        ],
    )
