
from common import *
import winsound

from Gomoku.Server import Server
from MCTS.Agent import DeepAgentMCTS

os.system("mode con cols=60 lines=35")
os.system('cls')


black = 500
white = 500


save_dir = 'selfplay_result/raw/'
save_path_base = '%d_%d_' % (black, white)

idx = 0
while os.path.exists(save_dir + save_path_base + str(idx) + '.txt'):
    idx += 1

if __name__ == '__main__':
    # for _ in range(2):
    save_path = save_path_base + str(idx) + '.txt'

    player_black = DeepAgentMCTS(black)
    player_white = DeepAgentMCTS(white)

    server = Server(player_black, player_white)

    server.run(log_path=save_dir + save_path)

    winsound.Beep(440, 300)

        # os.system('cls')
        # idx += 2


