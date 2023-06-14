import argparse
import numpy as np
from tqdm import tqdm

from src.game import Blackjack
from src.utils import Ploter

# 引数の設定
parser = argparse.ArgumentParser()
parser.add_argument("iterations", type=int, default=10000)
args = parser.parse_args()


def main():
    game = Blackjack()

    for i in tqdm(range(args.iterations)):
        (
            policy,
            q_state_usable_ace,
            count_q_state_usable_ace,
            q_state_no_usable_ace,
            count_q_state_no_usable_ace,
            q_hat_state_usable_ace,
            q_hat_state_no_usable_ace,
        ) = game.play()

    print("policy.ace: {}".format(policy.ace))
    print("policy.no_ace: {}".format(policy.no_ace))

    # プロット
    x = np.array(range(1, 11))
    y = np.array(range(12, 22))

    # 格子に乗る値
    ploter_ace = Ploter(x, y, np.array(policy.ace == "hit ", dtype=int))
    ploter_ace.plot_hit_or_stop("with_ace")

    ploter_No_ace = Ploter(x, y, np.array(policy.no_ace == "hit ", dtype=int))
    ploter_No_ace.plot_hit_or_stop("without_ace")


if __name__ == "__main__":
    main()
