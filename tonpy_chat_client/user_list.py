import flet as ft

def user_list_view(page: ft.Page):
    def go_to_chat(user_name):
        # 使用 `page.go` 跳转并传递用户名到路由
        page.go(f"/chat/{user_name}")

    return ft.View(
        "/users",
        [
            ft.AppBar(title=ft.Text("User List"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        title=ft.Text("QWEN"),
                        on_click=lambda _: go_to_chat("qwen"),  # 点击传递用户名
                    ),
                    ft.ListTile(
                        title=ft.Text("AI Bot"),
                        on_click=lambda _: go_to_chat("AIBot"),  # 传递其他用户名
                    ),
                ]
            ),
        ],
    )