
from common import *
import winsound

from Gomoku.Server import Server
from MCTS.Agent import DeepAgentMCTS, PureAgentMCTS

os.system("mode con cols=60 lines=35")
os.system('cls')


deep_agent_side = BLACK_
mul = 10

deep_cp = 500
pure_cp = deep_cp * mul


save_dir = 'selfplay_result/deep_pure/'
save_path_base = '%d_%d_%s_' % (deep_cp, pure_cp, 'B' if deep_agent_side == BLACK_ else 'W')

idx = 0
while os.path.exists(save_dir + save_path_base + str(idx) + '.txt'):
    idx += 1

if __name__ == '__main__':
    # for _ in range(2):
    save_path = save_path_base + str(idx) + '.txt'

    player_deep = DeepAgentMCTS(deep_cp)
    player_pure = PureAgentMCTS(pure_cp)

    if deep_agent_side == BLACK_:
        server = Server(player_deep, player_pure)
    else:
        server = Server(player_pure, player_deep)

    server.run(log_path=save_dir + save_path)

    winsound.Beep(440, 300)

        # os.system('cls')
        # idx += 2


