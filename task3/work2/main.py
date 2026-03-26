import matplotlib.pyplot as plt
import numpy as np

# Code by Gemini
# 我不知道怎么解决文字说明中文无法显示的问题，于是就问了哈基米
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
L = 1
k = 1
x0 = 0
x = np.linspace(-10, 10, 100)
y = L / (1 + np.exp(-k * (x - x0)))
if __name__ == "__main__":
    plt.plot(x, y)
    # 修改L的参数
    for i in np.arange(0, 2, 0.5):
        y1 = i / (1 + np.exp(-k * (x - x0)))
        plt.plot(x, y1, label=f"L={i}")
    # 修改k的参数
    for i in np.arange(0, 2, 0.5):
        y1 = L / (1 + np.exp(-i * (x - x0)))
        plt.plot(x, y1, label=f"k={i}")
    # 修改x0的参数
    for i in np.arange(-1, 1, 0.5):
        y1 = L / (1 + np.exp(-k * (x - i)))
        plt.plot(x, y1, label=f"x0={i}")
    plt.legend()
    plt.grid(True)
    plt.figtext(
        0.5,
        0.02,
        "L越大，曲线的上限越高，k越大，曲线越陡峭，x0越大，曲线越往右边移动",
        ha="center",
        fontsize=10,
        bbox={"facecolor": "white", "alpha": 0.2, "pad": 5},
    )
    # 留出底部空间，防止文字被切掉
    plt.subplots_adjust(bottom=0.15)
    plt.show()