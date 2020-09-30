
from common import *
import winsound

from Gomoku.Server import Server
from MCTS.Agent import DeepMCTSAgent

os.system("mode con cols=60 lines=35")
os.system('cls')


black = 1000
white = 2000


save_dir = 'selfplay_result/raw/'
save_path_base = '%d_%d_' % (black, white)

time_dir = 'selfplay_result/time_log/'

idx = 0
while os.path.exists(save_dir + save_path_base + str(idx) + '.txt'):
    idx += 1

if __name__ == '__main__':
    # for _ in range(2):
    save_path = save_path_base + str(idx) + '.txt'

    player_black = DeepMCTSAgent(black)
    player_white = DeepMCTSAgent(white)

    server = Server(player_black, player_white)

    server.run(log_path=save_dir + save_path, time_log_path=time_dir + save_path)
    # server.run(time_log_path=time_dir + save_path)

    winsound.Beep(440, 300)

        # os.system('cls')
        # idx += 2


