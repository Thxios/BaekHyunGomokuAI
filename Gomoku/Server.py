from common import *
from log import Log

from Gomoku.Board import Board
from Gomoku.Agent import AgentGUI, AgentCLI

from MCTS.Agent import DeepMCTSAgent, PureMCTSAgent


class Server:
    def __init__(
            self,
            player_black: Union[AgentCLI, AgentGUI, DeepMCTSAgent, PureMCTSAgent],
            player_white: Union[AgentCLI, AgentGUI, DeepMCTSAgent, PureMCTSAgent],
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

        self._time = {
            BLACK_: [],
            WHITE_: [],
        }

    @property
    def current_player(self):
        return self.player[self.board.current_player]


    def run(self, log_path=None, time_log_path=None):

        self.playing = True
        winner = None
        self.board.show()
        sys.stdout.flush()
        while self.playing:

            t1 = time.time()
            action = self.current_player.get_action(self.board)
            t2 = time.time()
            self._time[self.board.current_player].append(t2 - t1)

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
        if time_log_path is not None:
            if type(self.black) == DeepMCTSAgent:
                black_type = 'Deep MCTS Agent with compute budget %d' % self.black.compute_budget
            elif type(self.black) == PureMCTSAgent:
                black_type = 'Pure MCTS Agent with compute budget %d' % self.black.compute_budget
            else:
                black_type = 'Human Player'

            if type(self.white) == DeepMCTSAgent:
                white_type = 'Deep MCTS Agent with compute budget %d' % self.white.compute_budget
            elif type(self.white) == PureMCTSAgent:
                white_type = 'Pure MCTS Agent with compute budget %d' % self.white.compute_budget
            else:
                white_type = 'Human Player'

            with open(time_log_path, 'a') as f:
                f.write('Black player: ' + black_type + '\n')
                for black_time in self._time[BLACK_][1:]:
                    f.write('%.4f\n' % black_time)
                sum_black, len_black = sum(self._time[BLACK_][1:]), len(self._time[BLACK_]) - 1
                f.write('average: %.4fs per action\n' % (sum_black / len_black))
                if self.black.use_mcts:
                    f.write('         %.4fms per playout\n' % (sum_black * 1000 / len_black / self.black.compute_budget))
                f.write('\n')
                f.write('White player: ' + white_type + '\n')
                for white_time in self._time[WHITE_]:
                    f.write('%.4f\n' % white_time)
                sum_white, len_white = sum(self._time[WHITE_]), len(self._time[WHITE_])
                f.write('average: %.4fs per action\n' % (sum_white / len_white))
                if self.white.use_mcts:
                    f.write('         %.4fms per playout\n' % (sum_white * 1000 / len_white / self.white.compute_budget))



