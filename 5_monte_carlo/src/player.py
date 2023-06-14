import numpy as np
from src.utils import card_range_correcter


class Player:
    def __init__(self, policy: np.ndarray) -> None:
        # 持っているカードの和の推移
        self.player_sum_traj = [np.random.randint(12, 22)]
        # Aceの履歴
        self.Ace_flag_traj = [bool(np.random.choice([0, 1]))]
        # Actionの履歴
        self.action_traj = [np.random.choice(["hit ", "stop"])]

        # 方策
        self.policy = policy

        # 利用可能なエースがある時
        if self.Ace_flag_traj[0]:
            self.cards = [self.player_sum_traj[0] - 11, 11]  # 和から11を引いたものをもう一枚のカードとする
        else:
            temp = np.random.randint(2, 10)  # ない時は2-9のどれかを引く
            self.cards = [self.player_sum_traj[0] - temp, temp]

        self.init_flag = True

    def play(
        self, open_card: int
    ) -> tuple[list[int], list[bool], list[str], int]:  # opencardは補正して入力
        # dealerのカード
        self.open_card = open_card

        # スタンド判断
        stop_flag, score = self._judge_stop()

        # スタンドまでカードを引く
        while not stop_flag:
            self._draw()
            stop_flag, score = self._judge_stop()

        # 状態推移，Aceの推移，アクションの推移，最終的なscore
        return (
            self.player_sum_traj,
            self.Ace_flag_traj,
            self.action_traj,
            score,
        )

    def _judge_stop(self) -> tuple[bool, int]:  # ゲーム終了かどうか判断(player)
        # 初期化
        stop_flag = False

        # 今までの和をとる
        score = sum(self.cards)

        if self.init_flag:  # 初期状態
            # ランダムに生成した方策にしたがう
            if self.action_traj[0] == "stop":
                stop_flag = True

            self.init_flag = False

        else:  # 初期状態ではない
            while 11 in self.cards and score > 21:  # 21より大きくてAceを利用する場合
                self.cards[self.cards.index(11)] = 1  # 11を1として扱う
                score = sum(self.cards)

            # Aceを11で利用しているか判定
            if 11 in self.cards:
                Ace_flag = True
            else:
                Ace_flag = False

            # バースト判定
            if score > 21:
                stop_flag = True
                return stop_flag, score

            # エースの使い方を履歴に追加
            self.Ace_flag_traj.append(Ace_flag)

            # 履歴に現在の和を追加
            self.player_sum_traj.append(score)

            # 取ったアクションを履歴に追加
            self.action_traj.append(
                self.policy.get_action(
                    self.player_sum_traj[-1], self.Ace_flag_traj[-1], self.open_card
                )
            )

            # 方策にしたがう
            if (
                self.policy.get_action(
                    self.player_sum_traj[-1], self.Ace_flag_traj[-1], self.open_card
                )
                == "stop"
            ):
                stop_flag = True

        return stop_flag, score

    def _draw(self) -> None:  # カードを引く(player)
        draw_card = card_range_correcter(np.random.randint(1, 14))
        self.cards.append(draw_card)
