from common import *

from Gomoku.Agent import AgentCLI
from Gomoku.Server import Server

from MCTS.Agent import DeepMCTSAgent




if __name__ == '__main__':
    player1 = AgentCLI()
    # player2 = HumanPlayer()
    player2 = DeepMCTSAgent(100)
    server = Server(player2, player1)
    # server = Server(player1, player2)

    # for x, y in pre:
    #     server.play(move_xy2int(x, y))

    server.run()
