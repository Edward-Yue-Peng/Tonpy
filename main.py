import flet as ft
from chat_program.chat_client_class import *
from login import login_view
from chat import chat_view


def main(page: ft.Page):
    page.title = "Tonpy"
    page.views.append(login_view(page))
    page.session.set("exception", "")

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login_view(page))
            page.update()
        elif page.route == "/chat":
            try:
                page.views.append(chat_view(page))
                page.update()
                client = Client(page.session.get("server_addr"))
                client.init_chat()
                # if client.exception:
                #     page.session.set("exception", "server_addr")
                #     return ft.View(
                #         route="/chat",
                #         controls=[
                #             ft.AlertDialog(
                #                 modal=True,
                #                 content=ft.Text("Server address is not valid!"),
                #                 actions=[
                #                     ft.ElevatedButton(
                #                         text="Return to login page",
                #                         on_click=lambda _: page.overlay.pop(),
                #                     )
                #                 ],
                #             )
                #         ],
                #     )
                client_thread = threading.Thread(
                    target=client.run_chat, args=[page], daemon=True
                )
                client_thread.start()
                client.read_input(page.session.get("usrname"))
            except:
                page.go("/login")

    page.on_route_change = route_change
    page.go("/login")


ft.app(main)
