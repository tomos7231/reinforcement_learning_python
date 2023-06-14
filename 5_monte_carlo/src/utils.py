import numpy as np
import matplotlib.pyplot as plt


def card_range_correcter(card: int) -> int:
    # 絵札は10として扱う
    if card > 10:
        card = 10

    # Aは11として扱う
    if card == 1:
        card = 11

    return card


# 3Dgraphを作成するクラス
class Ploter:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
        # グラフ作成
        self.fig_2D = plt.figure()
        self.axis_2D = self.fig_2D.add_subplot(111)

    def plot_hit_or_stop(self, title: str) -> None:
        self.axis_2D.set_xlabel("dealer open card")
        self.axis_2D.set_ylabel("player sum")

        self.axis_2D.set_title(title)

        X, Y = np.meshgrid(self.x, self.y)

        Z = self.z

        img = self.axis_2D.pcolormesh(X, Y, Z, cmap="summer")

        pp = self.fig_2D.colorbar(img, orientation="vertical")  # カラーバーの表示
        pp.set_label("label")  # カラーバーの表示

        plt.show()
