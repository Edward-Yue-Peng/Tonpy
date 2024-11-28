import flet as ft
from user_list import user_list_view
from chat_page import chat_page_view
from login import login_view
from data_control import *

# 这玩意纯纯就是用来传各种参数，以及数据与后端的互动，其实应该有更聪明的办法，但是我不会。
data = Database()


def main(page: ft.Page):

    # Tony+py
    page.title = "Tonpy"

    def route_change(route):

        page.views.clear()

        # 跳转到登录页面，传递出来一个当前用户的名字
        if page.route == "/login" or page.route == "/":
            page.views.append(login_view(page, data))

        # 用户列表页面
        elif page.route == "/users":
            page.views.append(user_list_view(page, data))

        # 聊天页面
        elif page.route == "/chat" and data.selected_user is not None:
            page.views.append(chat_page_view(page, data))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
