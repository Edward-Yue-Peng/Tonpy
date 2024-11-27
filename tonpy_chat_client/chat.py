import flet as ft
from flet_core.colors import PRIMARY_CONTAINER
from flet_core.cupertino_colors import ON_PRIMARY


# 一条信息
class Message:
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type


class ChatMessage(ft.Row):
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
        self.controls = [ft.Container(
            content=single_message,
            # 控制一条信息的样式
            # border=ft.border.all(1, ft.colors.OUTLINE),
            # border_radius=5,
            # bgcolor=ON_PRIMARY,
            # padding=10,

            #TODO下面这条让自己发的信息右置
            # alignment = ft.alignment.center_right,
            expand=True,
        )
        ]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Tonpy"

    #TODO 不知道怎么改图标
    page.icon = 'assets/icon.png'
    # page.bgcolor = PRIMARY_CONTAINER
    # 加入聊天的控件
    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "Name cannot be blank!"
            join_user_name.update()
        else:
            #TODO用户名要传给后端
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            page.appbar = ft.AppBar(
                title=ft.Text(f"Welcome {join_user_name.value}! Let's chat."),
            )
            # new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(
                Message(
                    user_name=join_user_name.value,
                    text=f"{join_user_name.value} has joined the chat.",
                    message_type="login_message",
                )
            )
            page.update()

    # 发送键事件
    def send_message_click(e):
        #TODO发送的信息要传给后端
        if new_message.value != "":
            page.pubsub.send_all(
                Message(
                    page.session.get("user_name"),
                    new_message.value,
                    message_type="chat_message",
                )
            )
            new_message.value = ""
            new_message.focus()
            page.update()

    def more_button_click(e):
        pass

    # 发送信息的方法
    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # 进来先问用户名
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

    # 聊天区的占位
    chat = ft.ListView(
        expand=True,
        spacing=15,
        auto_scroll=True,
    )

    # 发新信息的输入框
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

    # 整个发送的控件
    sending_area = ft.Row(
        [
            ft.IconButton(
                icon=ft.icons.ADD,
                tooltip="More",
                on_click=more_button_click,
            ),
            new_message,
            ft.IconButton(
                icon=ft.icons.SEND_ROUNDED,
                tooltip="Send message",
                on_click=send_message_click,
            ),
        ]
    )

    page.add(
        ft.Container(
            content=chat,
            padding=10,
            expand=True,
        ), sending_area
        ,
    )


ft.app(target=main)
