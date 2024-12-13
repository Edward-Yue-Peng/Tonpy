import flet as ft
from chat_program.chat_client_class import *

BOARD_SIZE = 15


def gomoku_view(page: ft.Page, client: Client):
    page.title = "Gomoku"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    status = ft.Text("Welcome to Gomoku!", weight="bold")

    def on_quit(e):
        page.go("/chat")
        client.state = S_CHATTING

    def handle_click(e):
        x, y = e.control.data
        # 本地不立即更新UI和判断胜负，发送消息给服务器等待服务器返回gomoku_move
        if client.get_stone(x, y) == 0:
            client.read_input(f'gomoku_move {{"x":{x},"y":{y}}}')
            # 此处不更新UI，等待服务器返回gomoku_move消息才更新UI
            # 同时在外部有触发proc()的机制时会自动处理收到的消息并更新UI

    grid = ft.GridView(
        width=450,
        height=450,
        max_extent=30,
        expand=True,
        child_aspect_ratio=1.0,
        spacing=2,
        run_spacing=2,
    )

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cell = ft.Container(
                width=30,
                height=30,
                border=ft.border.all(1),
                data=(i, j),
                on_click=handle_click,
            )
            grid.controls.append(cell)

    return ft.View(
        route="/gomoku",
        controls=[
            ft.AppBar(
                title=ft.Text("Gomoku", weight="bold"),
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Quit",
                    on_click=on_quit,
                ),
            ),
            status,
            grid,
        ],
    )
