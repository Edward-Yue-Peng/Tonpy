import flet as ft
from chat_program.chat_client_class import *
from login import login_view
from chat import chat_view


def main(page: ft.Page):
    page.title = "Tonpy"
    page.views.append(login_view(page))

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page))
            page.update()
        elif page.route == "/chat":
            page.views.append(chat_view(page))
            page.update()

    page.on_route_change = route_change
    page.go("/login")


ft.app(main)
