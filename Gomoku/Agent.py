from common import *

from Gomoku.Board import Board


class _Agent:
    use_mcts = False
    gui = False

    def get_action(self, state: Board) -> int:
        raise NotImplementedError()


class AgentCLI(_Agent):
    def get_action(self, state: Board) -> int:
        while True:
            raw = input('action to move : ').lower().strip().replace(' ', '')
            try:
                x = ord(raw[0]) - 97
                y = int(raw[1:]) - 1
            except ValueError:
                print('invalid input format', raw)
                continue
            if x >= WIDTH or y >= HEIGHT or x < 0 or y < 0:
                print('invalid input range:', (x, y))
                continue

            move = move_xy2int(x, y)

            if state.check_valid(move):
                return move
            else:
                print('invalid action:', (x, y))
                continue


class AgentGUI(_Agent):
    gui = True

    def __init__(self, queue_move):
        self.queue_move = queue_move
        # self.queue_draw = queue_draw

    def get_action(self, state: Board) -> int:
        # last = state.last_move
        # if last != -1:
        #     last_x, last_y = move_int2xy(last)
        #     self.queue_draw.put((last_x, last_y, state.last_player))

        get_input = True
        move_int = -1
        while get_input:
            # print('get')
            try:
                x, y = self.queue_move.get()
            except TypeError:
                print('\n GUI window not found\n exit program\n')
                time.sleep(1)
                sys.exit()
            # print((x, y))
            move_int = move_xy2int(x, y)
            if state.check_valid(move_int):
                get_input = False
                # print('valid')

        # self.queue_draw.put((x, y, state.current_player))

        return move_int

