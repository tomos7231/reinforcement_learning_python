import numpy as np

from src.utils import card_range_correcter


class Dealer:
    def __init__(self) -> None:
        # 見えているカード
        self.open = card_range_correcter(np.random.randint(1, 11))
        # 見せていないほうのカード
        self.cards = [self.open, card_range_correcter(np.random.randint(1, 14))]

    def play(self):  # ゲームをする
        stop_flag, score = self._judge_stop()  # スタンドかどうか判断

        while not stop_flag:  # スタンドまではカードを引く
            self._draw()
            stop_flag, score = self._judge_stop()

        return self.open, score  # 開いてるカードと数字の合計を返す

    def _judge_stop(self) -> tuple[bool, int]:  # ストップかどうか判断
        # 初期化
        stop_flag = False

        # 和をとる
        score = sum(self.cards)

        # 大きさ確認
        while 11 in self.cards and score > 21:  # 21より大きくてAceを利用する場合
            self.cards[self.cards.index(11)] = 1  # 1を代入
            score = sum(self.cards)

        # 17以上だとdealerはストップ
        if score >= 17:
            stop_flag = True

        return stop_flag, score

    def _draw(self):  # カードを引く(dealer)
        draw_card = card_range_correcter(np.random.randint(1, 14))
        self.cards.append(draw_card)
