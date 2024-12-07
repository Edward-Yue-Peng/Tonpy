import flet as ft
from data_control import Database
import json
import threading
from chat_utils import *

def login_view(page: ft.Page, data: Database):
    # 登录按钮事件
    def on_login_click(e):
        if not user_name.value.strip():
            user_name.error_text = "Name cannot be blank!"
            user_name.update()
        else:
            user_name_str = user_name.value.strip()
            # 记录用户名到 data 并跳转到用户列表
            data.user_name = user_name_str
            # 跳转到用户列表并在 console 输出用户名
            print(f"Logged in as {user_name_str}")
            data.state = "online"
            # 与后端交互
            msg = json.dumps({"action": "login", "name": user_name_str})
            mysend(data.socket,msg)
            response = json.loads(myrecv(data.socket))
            if response.get("status") == "ok":
                # 登录成功，跳转到用户列表页面
                print(f"Logged in as {user_name_str}")
                data.state = "online"
                page.go("/users")
            else:
                # 登录失败，显示错误信息
                user_name.error_text = "Login failed: " + response.get("status", "Unknown error")
                user_name.update()
                page.go("/users")  # 登录后跳转到用户列表

    # 用户名输入框
    user_name = ft.TextField(
        label="Enter your name to join",
        autofocus=True,
        expand=True,
        on_submit=on_login_click,
    )

    # 登录按钮
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=on_login_click,
    )

    # 返回视图
    return ft.View(
        route="/login",
        appbar=ft.AppBar(
            title=ft.Text("Login"),
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        user_name,
                        login_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
                padding=20,
            )
        ],
    )
