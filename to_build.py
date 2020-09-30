
# if __name__ == '__main__':
from common import *
# print(__name__)
# time.sleep(3)
os.system('cls')
os.system("mode con cols=60 lines=35")
print('\n\n  Now loading...')

import multiprocessing as mp
# os.system('cls')
# from multiprocessing import Process, Queue


def start(q1, q2, cp):
    from Gomoku.GUI import BoardWindow
    q2.get()
    # print(__name__)
    window = BoardWindow(queue_move=q1, queue_draw=q2)
    window.title('Baekhyun Gomoku AI - compute budget: ' + str(cp))
    window.run()


def load_config():
    # with open('./settings.txt', 'r') as f:
    with open(os.path.dirname(os.getcwd()) + '\\settings.txt', 'r') as f:
        lines = f.readlines()

    c_budget = int(lines[0].split(':')[1])
    color = lines[1].split(':')[1].lower().strip()

    if color not in ('b', 'w'):
        raise ValueError

    return max(c_budget, 100), color == 'b'


if __name__ == '__main__':
    mp.freeze_support()
    # os.system('cls')
    try:
        compute_budget, ai_color = load_config()
    except Exception:
        print(' fail to load settings.')
        print(' please make sure the settings.txt file is valid format.')
        print(' start with default setting...')
        print(' compute budget: 1000')
        print(' AI plays on black side')
        time.sleep(3)
        compute_budget = 1000
        ai_color = True


    q_move = mp.Queue()
    q_draw = mp.Queue()
    gui_handler = mp.Process(target=start, args=(q_move, q_draw, compute_budget))
    gui_handler.start()


    from Gomoku.Agent import AgentGUI
    from Gomoku.Server import Server
    from MCTS.Agent import DeepMCTSAgent
    os.system('cls')


    player1 = AgentGUI(queue_move=q_move)
    player2 = DeepMCTSAgent(compute_budget)
    # os.system('cls')
    if ai_color:
        server = Server(player2, player1, queue_draw=q_draw)
    else:
        server = Server(player1, player2, queue_draw=q_draw)

    # window = BoardWindow(queue=queue)

    q_draw.put(True)
    server.run()

    # input()
