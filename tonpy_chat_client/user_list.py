import flet as ft
from data_control import Database


def user_list_view(page: ft.Page, data: Database):
    def on_select_user(user):
        # 跳转到聊天页面并在 console 输出用户名
        print(f"Chat with {user}")
        data.selected_user = user
        data.state = "chatting"
        page.go(f"/chat")

    def on_logout(e):
        print(f"{data.user_name} logged out")
        data.state = "offline"
        data.user_name = None
        page.go("/login")

    return ft.View(
        "/users",
        [
            ft.AppBar(
                title=ft.Text(f"Welcome {data.user_name}", weight="bold"),
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    tooltip="Logout",
                    # 注销账户
                    on_click=on_logout,
                ),
            ),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        title=ft.Text(user),
                        # 这里tm也是玄学，不知道为什么一定要用lambda，我正常用函数就出bug，GPT告诉我的，不知道为啥
                        on_click=lambda e, u=user: on_select_user(u),
                    )
                    for user in data.user_list
                ]
            ),
        ],
    )
