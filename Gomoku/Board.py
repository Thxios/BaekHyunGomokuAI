from common import *


class Board:
    def __init__(self):
        self.current_player = BLACK_
        self.last_player = WHITE_
        self.available = set(range(WIDTH * HEIGHT))
        self.moved: List[int] = []
        self.board = np.zeros((WIDTH, HEIGHT, 2), dtype=np.float32)
        self.last_move: int = -1

        self.must: List[Set[int]] = [set(), set()]

    def __del__(self):
        del self.board
        del self.moved
        del self.available

    def _get_color(self, x, y, color):
        if x < 0 or x >= WIDTH:
            return -1
        if y < 0 or y >= HEIGHT:
            return -1

        return self.board[x, y, color]

    def copy(self):
        return copy.deepcopy(self)

    def set(self, move: int):
        x, y = move_int2xy(move)
        self.board[x, y, self.current_player] = 1

    def get_board_array(self) -> np.ndarray:
        if self.current_player == BLACK_:
            return self.board[:, :, (1, 0)]
        elif self.current_player == WHITE_:
            return self.board

    def is_empty(self) -> bool:
        return len(self.moved) == 0

    def check_valid(self, move: int) -> bool:
        if move < 0 or move >= WIDTH * HEIGHT:
            return False
        # if move in self.moved:
        #     return False

        return move in self.available

    def play(self, move: int) -> bool:
        if not self.check_valid(move):
            return False
            # raise ValueError('Not valid move')

        if move in self.must[0]:
            self.must[0].remove(move)
        if move in self.must[1]:
            self.must[1].remove(move)

        self.set(move)
        self.available.remove(move)
        self.moved.append(move)
        self.last_move = move
        self.change_player()

        # ----- for test -----
        self._four_in_row()
        # print(self.must)

        return True

    def undo(self) -> bool:
        if len(self.moved) == 0:
            return False

        row, column = move_int2xy(self.last_move)
        self.board[row, column, :] = 0
        self.available.add(self.last_move)
        self.moved.pop()
        if len(self.moved) == 0:
            self.last_move = -1
        else:
            self.last_move = self.moved[-1]
        self.change_player()

        return True

    def change_player(self):
        self.last_player = self.current_player
        self.current_player = WHITE_ if self.current_player == BLACK_ else BLACK_
        # self.current_player = 1 - self.current_player

    def _five_in_row(self) -> Union[int, None]:
        if len(self.moved) < 2 * 5 - 1:
            return None

        last_x, last_y = move_int2xy(self.last_move)

        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0)):
            cnt = 1
            x, y = last_x, last_y
            while self._get_color(x + dx, y + dy, self.last_player) == 1:
                x += dx
                y += dy
                cnt += 1
            x, y = last_x, last_y
            while self._get_color(x - dx, y - dy, self.last_player) == 1:
                x -= dx
                y -= dy
                cnt += 1

            if cnt >= 5:
                return self.last_player

        return None

    def _four_in_row(self):
        last_x, last_y = move_int2xy(self.last_move)
        # self.must[self.last_player] = -1

        for dx, dy in ((-1, -1), (0, -1), (1, -1), (1, 0)):
            cnt = 1
            x, y = (last_x, last_y)

            left_cnt, right_cnt = 0, 0
            left_end, right_end = None, None
            while self._get_color(x + dx, y + dy, self.last_player) == 1:
                x += dx
                y += dy
                cnt += 1
            if self._get_color(x + dx, y + dy, self.current_player) == 0:
                x += dx
                y += dy
                left_end = move_xy2int(x, y)
                while self._get_color(x + dx, y + dy, self.last_player) == 1:
                    x += dx
                    y += dy
                    left_cnt += 1

            x, y = (last_x, last_y)
            while self._get_color(x - dx, y - dy, self.last_player) == 1:
                x -= dx
                y -= dy
                cnt += 1
            if self._get_color(x - dx, y - dy, self.current_player) == 0:
                x -= dx
                y -= dy
                right_end = move_xy2int(x, y)
                while self._get_color(x - dx, y - dy, self.last_player) == 1:
                    x -= dx
                    y -= dy
                    right_cnt += 1

            # print((last_x, last_y), cnt, left_cnt, right_cnt,
            #       None if left_end is None else move_int2xy(left_end),
            #       None if right_end is None else move_int2xy(right_end))

            if cnt == 4:
                if left_end is not None:
                    self.must[self.last_player].add(left_end)
                if right_end is not None:
                    self.must[self.last_player].add(right_end)
            elif left_end is not None and cnt + left_cnt == 4:
                self.must[self.last_player].add(left_end)
            elif right_end is not None and cnt + right_cnt == 4:
                self.must[self.last_player].add(right_end)

    def check_winner(self) -> Tuple[bool, Union[int, None]]:
        # must be called right after every moves
        winner = self._five_in_row()
        if winner is not None:
            # print(winner, 'win')
            return True, winner
        elif not self.available:
            return True, None
        else:
            return False, None

    def check_must(self):
        if self.must[self.current_player]:
            return self.must[self.current_player].pop()
        if self.must[self.last_player]:
            return self.must[self.last_player].pop()
        return None

    def show(self):
        char = {
            (1, 0): 'X',    # black
            (0, 1): 'O',    # white
            (0, 0): '.'     # empty
        }

        print('    ', end='')
        for x in range(WIDTH):
            print(chr(x + 97), end='  ')
        print('\n', end='')
        for y in range(HEIGHT):
            if y + 1 > 9:
                print(y + 1, end='  ')
            else:
                print('', y + 1, end='  ')
            for x in range(WIDTH):
                print(char[self.board[x, y, BLACK_], self.board[x, y, WHITE_]], end='  ')
            print('\n', end='')
        print(' ')

        sys.stdout.flush()
        # time.sleep(0.5)


if __name__ == '__main__':
    pass


