import flet as ft
from chat_program.chat_client_class import *

BOARD_SIZE = 15


def gomoku_view(page: ft.Page, client: Client):
    page.title = "Gomoku"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    # status = ft.Text("当前玩家：黑棋", size=20)
    game_over = False

    def on_quit(e):
        page.go("/chat")
        client.state = S_CHATTING
        # TODO: quit game

    def check_winner(x, y, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for step in range(1, 5):
                nx, ny = x + dx * step, y + dy * step
                if (
                    0 <= nx < BOARD_SIZE
                    and 0 <= ny < BOARD_SIZE
                    and board[nx][ny] == player
                ):
                    count += 1
                else:
                    break
            for step in range(1, 5):
                nx, ny = x - dx * step, y - dy * step
                if (
                    0 <= nx < BOARD_SIZE
                    and 0 <= ny < BOARD_SIZE
                    and board[nx][ny] == player
                ):
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False

    def handle_click(e):
        nonlocal game_over
        if game_over:
            return
        x, y = e.control.data
        # client.read_input(f'gomoku_move {{"x":{x},"y":{y}}}')
        if board[x][y] == 0:
            board[x][y] = 1
            e.control.content = ft.Container(
                width=20,
                height=20,
                bgcolor="red",
                border_radius=10,
            )
            client.read_input(f'gomoku_move {{"x":{x},"y":{y}}}')
            # if check_winner(x, y, 1):
            #         status.value = "黑棋胜利！"
            #         game_over = True
            #     else:
            #         status.value = "当前玩家：白棋"
            # if status.value == "当前玩家：黑棋":
            #     board[x][y] = 1
            #     e.control.content = ft.Container(
            #         width=20,
            #         height=20,
            #         bgcolor="red",
            #         border_radius=10,
            #     )
            #     if check_winner(x, y, 1):
            #         status.value = "黑棋胜利！"
            #         game_over = True
            #     else:
            #         status.value = "当前玩家：白棋"
            # else:
            #     board[x][y] = 2
            #     e.control.content = ft.Container(
            #         width=20,
            #         height=20,
            #         bgcolor="red",
            #         border_radius=10,
            #     )
            #     if check_winner(x, y, 2):
            #         status.value = "白棋胜利！"
            #         game_over = True
            #     else:
            #         status.value = "当前玩家：黑棋"
            page.update()

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
                title=ft.Text(f"gomoku", weight="bold"),
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    tooltip="Quit",
                    on_click=on_quit,
                ),
            ),
            grid,
        ],
    )
