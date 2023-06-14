import numpy as np
from src.policy import Policy
from src.player import Player
from src.dealer import Dealer


class Blackjack:
    def __init__(self) -> None:
        # 利用可能なエースがある時
        # プレイヤーは12〜21の10通りの値を取り、ディーラーのカードは1〜10の10通りの値を取る
        self.value_state_usable_ace = np.array(
            [[0.0 for i in range(10)] for k in range(10)]
        )
        # 利用可能なエースがない時
        self.value_state_no_usable_ace = np.array(
            [[0.0 for i in range(10)] for k in range(10)]
        )

        # 訪問回数を記録
        self.count_value_state_useable_ace = np.array(
            [[0 for i in range(10)] for k in range(10)]
        )
        self.count_value_state_no__useable_ace = np.array(
            [[0 for i in range(10)] for k in range(10)]
        )

        # 行動価値
        self.q_state_usable_ace = np.array(
            [[[0.0, 0.0] for i in range(10)] for k in range(10)]
        )
        self.q_state_no_usable_ace = np.array(
            [[[0.0, 0.0] for i in range(10)] for k in range(10)]
        )

        # 訪問回数を記録
        self.count_q_state_usable_ace = np.array(
            [[[0, 0] for i in range(10)] for k in range(10)]
        )
        self.count_q_state_no_usable_ace = np.array(
            [[[0, 0] for i in range(10)] for k in range(10)]
        )

        # 推定した行動価値
        self.q_hat_state_usable_ace = np.array(
            [[[0.0, 0.0] for i in range(10)] for k in range(10)]
        )
        self.q_hat_state_no_usable_ace = np.array(
            [[[0.0, 0.0] for i in range(10)] for k in range(10)]
        )

        # 方策
        self.policy = Policy()

    def play(self):
        # 各プレイヤー
        self.dealer = Dealer()
        self.player = Player(self.policy)

        # ディーラーがカードを引く
        card_open, score_dealer = self.dealer.play()

        # 数字補正
        if card_open == 11:
            card_open = 1

        # プレイヤーがカードを引く
        player_sum_traj, ace_flag_traj, action_traj, score_player = self.player.play(
            card_open
        )

        # 報酬の計算
        reward = self._reward(score_dealer, score_player)

        # 保存
        card_open = card_open - 1

        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] > 21 or player_sum_traj[i] < 12:
                continue

            action = action_traj[i]
            if action == "hit ":
                action = 0
            else:
                action = 1

            player_sum = player_sum_traj[i] - 12

            if ace_flag_traj[i]:
                # 報酬の履歴の追加
                self.q_state_usable_ace[player_sum, card_open, action] += reward
                self.count_q_state_usable_ace[player_sum, card_open, action] += 1

            else:
                self.q_state_no_usable_ace[player_sum, card_open, action] += reward
                self.count_q_state_no_usable_ace[player_sum, card_open, action] += 1

        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] > 21 or player_sum_traj[i] < 12:
                continue

            action = action_traj[i]
            if action == "hit ":
                action = 0
            else:
                action = 1

            player_sum = player_sum_traj[i] - 12

            # 推定報酬（平均）の計算
            if ace_flag_traj[i]:
                self.q_hat_state_usable_ace[player_sum, card_open, action] = (
                    self.q_state_usable_ace[player_sum, card_open, action]
                    / self.count_q_state_usable_ace[player_sum, card_open, action]
                )
            else:
                self.q_hat_state_no_usable_ace[player_sum, card_open, action] = (
                    self.q_state_no_usable_ace[player_sum, card_open, action]
                    / self.count_q_state_no_usable_ace[player_sum, card_open, action]
                )

        # 方策の改善
        self.policy.improve(
            player_sum_traj,
            ace_flag_traj,
            card_open,
            self.q_hat_state_usable_ace,
            self.q_hat_state_no_usable_ace,
        )

        return (
            self.policy,
            self.q_state_usable_ace,
            self.count_q_state_usable_ace,
            self.q_state_no_usable_ace,
            self.count_q_state_no_usable_ace,
            self.q_hat_state_usable_ace,
            self.q_hat_state_no_usable_ace,
        )

    def _reward(self, dealer_score: int, player_score: int) -> int:  # 価値計算
        if player_score > 21:  # 自分がくず手なら負け
            reward = -1.0
        else:
            if dealer_score > 21:  # dealerがくず手の時点で勝ち
                reward = 1.0
            else:
                if player_score > dealer_score:  # player勝ち
                    reward = 1.0
                elif player_score < dealer_score:  # dealer勝ち
                    reward = -1.0
                elif player_score == dealer_score:
                    reward = 0.0  # 引き分け

        return reward
