from common import BLACK_, WHITE_
import sys
import tkinter as tk


class BoardCanvas(tk.Canvas):
    radius = 12

    def __init__(
            self,
            queue_move=None,
            master=None,
            height=0, width=0
    ):
        tk.Canvas.__init__(self, master, height=height, width=width)
        self.queue = queue_move
        self.draw_board()
        self.previous_action = []
        self.prevent_input = 0

    def draw_board(self):
        # 15 horizontal lines
        for i in range(15):
            start_pixel_x = (i + 1) * 30
            start_pixel_y = (0 + 1) * 30
            end_pixel_x = (i + 1) * 30
            end_pixel_y = (14 + 1) * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        # 15 vertical lines
        for j in range(15):
            start_pixel_x = (0 + 1) * 30
            start_pixel_y = (j + 1) * 30
            end_pixel_x = (14 + 1) * 30
            end_pixel_y = (j + 1) * 30
            self.create_line(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y)

        self.draw_star(3, 3)
        self.draw_star(11, 3)
        self.draw_star(7, 7)
        self.draw_star(3, 11)
        self.draw_star(11, 11)

    def draw_star(self, x, y):
        start_pixel_x = (x + 1) * 30 - 2
        start_pixel_y = (y + 1) * 30 - 2
        end_pixel_x = (x + 1) * 30 + 2
        end_pixel_y = (y + 1) * 30 + 2

        self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')

    def draw_stone(self, x, y, turn):
        inner_start_x = (x + 1) * 30 - 5
        inner_start_y = (y + 1) * 30 - 5
        inner_end_x = (x + 1) * 30 + 5
        inner_end_y = (y + 1) * 30 + 5

        outer_start_x = (x + 1) * 30 - 7
        outer_start_y = (y + 1) * 30 - 7
        outer_end_x = (x + 1) * 30 + 7
        outer_end_y = (y + 1) * 30 + 7

        start_pixel_x = (x + 1) * 30 - self.radius
        start_pixel_y = (y + 1) * 30 - self.radius
        end_pixel_x = (x + 1) * 30 + self.radius
        end_pixel_y = (y + 1) * 30 + self.radius

        if turn == BLACK_:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='white')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='black')
        elif turn == WHITE_:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')
            self.create_oval(outer_start_x, outer_start_y, outer_end_x, outer_end_y, fill='black')
            self.create_oval(inner_start_x, inner_start_y, inner_end_x, inner_end_y, fill='white')

    def draw_prev_stone(self, x, y, turn):
        start_pixel_x = (x + 1) * 30 - self.radius
        start_pixel_y = (y + 1) * 30 - self.radius
        end_pixel_x = (x + 1) * 30 + self.radius
        end_pixel_y = (y + 1) * 30 + self.radius

        if turn == BLACK_:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='black')
        elif turn == WHITE_:
            self.create_oval(start_pixel_x, start_pixel_y, end_pixel_x, end_pixel_y, fill='white')

    def put_stone(self, x, y, turn):
        self.draw_stone(x, y, turn)

        if len(self.previous_action):
            pre_x, pre_y, pre_turn = self.previous_action[-1]
            self.draw_prev_stone(pre_x, pre_y, pre_turn)

        self.previous_action.append((x, y, turn))
        self.prevent_input -= 1

    def on_board_clicked(self, event):
        if self.prevent_input == 1:
            return

        clicked_x, clicked_y = (event.x - 15) // 30, (event.y - 15) // 30
        # print((clicked_x, clicked_y))
        error_x, error_y = event.x - (clicked_x + 1) * 30, event.y - (clicked_y + 1) * 30
        if abs(error_x) > 10 or abs(error_y) > 10:
            return 0
        if clicked_x < 0 or clicked_x >= 15 or clicked_y < 0 or clicked_y >= 15:
            return 0

        # print((clicked_x, clicked_y))
        self.prevent_input = 2
        self.queue.put((clicked_x, clicked_y))


class BoardFrame(tk.Frame):
    def __init__(
            self,
            queue_move,
            master=None,
    ):
        tk.Frame.__init__(self, master)
        self.board_canvas = BoardCanvas(height=550, width=480, queue_move=queue_move)
        self.board_canvas.bind('<Button-1>', self.board_canvas.on_board_clicked)
        self.board_canvas.pack()


class BoardWindow(tk.Tk):
    def __init__(self, queue_move=None, queue_draw=None):
        super().__init__()

        self.queue_move = queue_move
        self.queue_draw = queue_draw
        self.board = BoardFrame(queue_move=self.queue_move, master=self)
        self.board.pack()

    def run(self):
        while True:
            try:
                self.update_idletasks()
                self.update()
            except:
                self.queue_move.put(-1)
                sys.exit()

            try:
                x, y, turn = self.queue_draw.get(timeout=0.05)
                self.board.board_canvas.put_stone(x, y, turn)
            except Exception:
                continue
