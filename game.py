import flet as ft


def game_view(page: ft.Page, client):
    def on_select_game(e):
        page.go(f"/chat")

    def on_quit(e):
        page.go("/chat")
        # TODO: quit game

    return ft.View(
        route="/game",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Gaming", weight="bold"),
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    tooltip="Logout",
                    on_click=on_quit,
                ),
            ),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        title=ft.Text("haha"),
                        on_click=on_select_game,
                    ),
                    ft.ListTile(
                        title=ft.Text("haha1"),
                        on_click=on_select_game,
                    ),
                ]
            ),
        ],
    )
