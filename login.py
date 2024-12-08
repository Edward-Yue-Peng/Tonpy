import flet as ft


def login_view(page: ft.Page):
    def on_login_click(e):
        if not usrname.value.rstrip():
            usrname.error_text = "Name cannot be blank!"
            usrname.update()
        else:
            page.session.set("server_addr", server_addr.value)
            page.session.set("usrname", usrname.value)
            print(f"Logged in as {usrname.value}")
            page.go("/chat")

    server_addr = ft.TextField(label="Server address", hint_text="localhost")
    usrname = ft.TextField(label="Username")

    login_button = ft.ElevatedButton(
        text="Login",
        on_click=on_login_click,
    )

    return ft.View(
        route="/login",
        appbar=ft.AppBar(
            title=ft.Text("Login"),
        ),
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        server_addr,
                        usrname,
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
