from common import *


if __name__ == '__main__':
    os.system("mode con cols=60 lines=35")
    print('\n\n  Now loading...')
    from Gomoku.Agent import AgentGUI
    from Gomoku.Server import Server
    from MCTS.Agent import DeepMCTSAgent, PureMCTSAgent

    from multiprocessing import Process, Queue

if __name__ == '__mp_main__':
    from Gomoku.GUI import BoardWindow


def start(q1, q2):
    time.sleep(0.2)
    BoardWindow(queue_move=q1, queue_draw=q2).run()


if __name__ == '__main__':
    q_move = Queue()
    q_draw = Queue()
    player1 = AgentGUI(queue_move=q_move)
    player2 = DeepMCTSAgent(500)
    # player2 = PureAgentMCTS(1000)
    server = Server(player2, player1, queue_draw=q_draw)
    # server = Server(player1, player2, queue_draw=q_draw)

    # window = BoardWindow(queue=queue)

    gui_handler = Process(target=start, args=(q_move, q_draw))
    gui_handler.start()
    server.run()
