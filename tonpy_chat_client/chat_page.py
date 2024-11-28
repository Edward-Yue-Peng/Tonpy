import flet as ft
from chat_control import chat_with_individual
from data_control import Database


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


def chat_page_view(page: ft.Page, data: Database):
    def send_message_click(e):
        if new_message.value.strip():
            # 这里是因为，如果直接用value，gpt反应时间会很慢，变成聊天栏很久不清除
            user_message = new_message.value.strip()
            new_message.value = ""
            new_message.focus()

            # 添加用户发送的消息到聊天列表
            chat.controls.append(
                ChatMessageSent(Message(data.user_name, user_message, "sent_message"))
            )
            page.update()

            # 获取回复并添加到聊天列表
            #TODO 这里的聊天逻辑是明显有问题的
            response = chat_with_individual(user_message)
            chat.controls.append(
                ChatMessageReceive(
                    Message(data.selected_user, response, "received_message")
                )
            )
            page.update()

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
        route="/chat",
        appbar=ft.AppBar(
            title=ft.Text(f"Chat with {data.selected_user}"),
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
