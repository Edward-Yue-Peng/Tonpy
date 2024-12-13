import threading
import flet as ft
from chat_program.chat_client_class import *
from login import login_view
from chat import chat_view
from gomoku import gomoku_view


def main(page: ft.Page):
    page.title = "Tonpy"
    page.views.append(login_view(page))
    page.session.set("exception", "")

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page))
            page.session.set("needs_client", True)
            page.update()
        elif page.route == "/chat":
            if page.session.get("needs_client"):
                global client
                client = Client(page.session.get("server_addr"))
                page.views.append(chat_view(page, client))
                page.update()
                client.init_chat()
                client_thread = threading.Thread(
                    target=client.run_chat, args=[page], daemon=True
                )
                client_thread.start()
                client.read_input(page.session.get("usrname"))
                page.session.set("needs_client", False)

            else:
                page.views.append(chat_view(page, client))
                page.update()
        elif page.route == "/gomoku":
            page.views.append(gomoku_view(page, client))
            page.session.set("needs_client", False)
            page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")


ft.app(main)
