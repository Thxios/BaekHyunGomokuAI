from common import *

from Gomoku.Board import Board
from Gomoku.Agent import AgentGUI, AgentCLI

from MCTS.Agent import DeepAgentMCTS, PureAgentMCTS
from MCTS.log import Log



class Server:
    def __init__(
            self,
            player_black: Union[AgentCLI, AgentGUI, DeepAgentMCTS, PureAgentMCTS],
            player_white: Union[AgentCLI, AgentGUI, DeepAgentMCTS, PureAgentMCTS],
            queue_draw=None
    ):
        self.board = Board()

        self.black = player_black
        self.white = player_white

        self.player = {
            BLACK_: self.black,
            WHITE_: self.white
        }

        self.queue_draw = queue_draw
        self.playing = False
        if self.black.gui or self.white.gui:
            self.gui = True
        else:
            self.gui = False

    @property
    def current_player(self):
        return self.player[self.board.current_player]


    def run(self, log_path=None):

        self.playing = True
        winner = None
        self.board.show()
        sys.stdout.flush()
        while self.playing:
            action = self.current_player.get_action(self.board)

            if log_path is not None:
                with open(log_path, 'a') as f:
                    f.write(str(move_int2xy(action)) + '\n')

            self.board.play(action)

            os.system('cls')
            self.board.show()
            Log.flush()
            sys.stdout.flush()
            if self.gui:
                self.queue_draw.put((*move_int2xy(action), self.board.last_player))

            is_end, winner = self.board.check_winner()
            if is_end:
                self.playing = False

        if winner is None:
            print(' Game Draw')
        elif winner == BLACK_:
            print(' Black win')
        elif winner == WHITE_:
            print(' White win')

        if log_path is not None:
            with open(log_path, 'a') as f:
                if winner is None:
                    f.write('Game Draw\n')
                elif winner == BLACK_:
                    f.write('Black win\n')
                elif winner == WHITE_:
                    f.write('White win\n')



