import numpy as np


class Policy:
    def __init__(self) -> None:
        # 行がプレイヤーの和（12-21），列がディラーのopenカード（1-10）
        self.ace = np.array([["hit " for i in range(10)] for k in range(10)])
        self.no_ace = np.array([["hit " for i in range(10)] for k in range(10)])
        # 初期方策ではプレイヤーは20, 21の時にカードを引かない
        self.ace[8:, :] = np.array([["stop" for i in range(10)] for k in range(2)])
        self.no_ace[8:, :] = np.array([["stop" for i in range(10)] for k in range(2)])

    def get_action(self, player_sum: int, Ace_flag: bool, open_card: int) -> str:
        # 値修正
        open_card = open_card - 1
        player_sum = player_sum - 12

        if Ace_flag:
            # プレイヤーのカード合計は12始まり、ディーラーのopenカードは1始まりなのでindex合わせる
            return self.ace[player_sum, open_card]
        else:
            return self.no_ace[player_sum, open_card]

    def improve(
        self,
        player_sum_traj: list[int],
        Ace_traj: list[bool],
        open_card: int,
        ave_Q_state_Ace: np.ndarray,
        ave_Q_state_No_Ace: np.ndarray,
    ):
        for i in range(len(player_sum_traj)):
            if (
                player_sum_traj[i] > 21 or player_sum_traj[i] < 12
            ):  # 22以上と11以下はいれてもしょうがないのでパス
                continue

            # 値修正
            player_sum = player_sum_traj[i] - 12

            if Ace_traj[i]:
                # hitの方が良い場合
                if (
                    ave_Q_state_Ace[player_sum, open_card, 0]
                    > ave_Q_state_Ace[player_sum, open_card, 1]
                ):
                    self.ace[player_sum, open_card] = "hit "
                # standの方が良い場合
                elif (
                    ave_Q_state_Ace[player_sum, open_card, 0]
                    < ave_Q_state_Ace[player_sum, open_card, 1]
                ):
                    self.ace[player_sum, open_card] = "stop"
            else:
                # hitの方が良い場合
                if (
                    ave_Q_state_No_Ace[player_sum, open_card, 0]
                    > ave_Q_state_No_Ace[player_sum, open_card, 1]
                ):
                    self.no_ace[player_sum, open_card] = "hit "
                # standの方が良い場合
                elif (
                    ave_Q_state_No_Ace[player_sum, open_card, 0]
                    < ave_Q_state_No_Ace[player_sum, open_card, 1]
                ):
                    self.no_ace[player_sum, open_card] = "stop"
