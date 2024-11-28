import flet as ft
from user_list import user_list_view
from chat_page import chat_page_view


def main(page: ft.Page):
    page.title = "Tonpy"

    def route_change(route):
        page.views.clear()

        # 用户列表
        if page.route == "/" or page.route == "/users":
            page.views.append(user_list_view(page))
        # 聊天页面
        elif page.route.startswith("/chat/"):
            page.views.append(chat_page_view(page))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
