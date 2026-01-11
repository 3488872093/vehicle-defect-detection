import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from PySide6.QtCore import QThread

class PlottingThread(QThread):
    def __init__(self, result_statistic, workpath):
        super().__init__()
        self.result_statistic = result_statistic
        self.workpath = workpath

    def run(self):
        # 设置字体和坐标轴样式
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams["xtick.major.size"] = 0
        plt.rcParams["ytick.major.size"] = 0

        # 数据计算
        total = sum(self.result_statistic.values())
        percentages = {k: (v / total * 100) for k, v in self.result_statistic.items()}

        # 准备数据
        activities = list(percentages.keys())
        values = list(percentages.values())

        # 创建图形和坐标轴，调整画布大小
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

        # 绘制柱状图
        bars = sns.barplot(x=activities, y=values, ax=ax, zorder=3)
        ax.set_xlabel("类别", fontsize=16, labelpad=5)
        ax.set_ylabel("百分比 (%)", fontsize=16, labelpad=5)

        # 根据值设置柱状图颜色，并调整数据标签位置和字体大小
        for bar, value in zip(ax.patches, values):
            if value <= 25:
                bar.set_color("#9dc1c5")  # 浅蓝色
            elif value >= 75:
                bar.set_color("#d7a6b3")  # 浅红色
            else:
                bar.set_color("#8e93af")  # 正常颜色

            # 添加数据标签（修改以下部分）
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                bar.get_height() + 1,  # 将标签移动到柱顶上方
                f"{value:.1f}%",
                ha="center",
                va="bottom",  # 底部对齐确保文本在柱顶上方
                color="black",  # 改为黑色字体
                fontsize=16
            )

        # 添加水平参考线
        ax.axhline(y=25, color="#9dc1c5", linestyle="--", linewidth=1, zorder=2)
        ax.axhline(y=75, color="#d7a6b3", linestyle="--", linewidth=1, zorder=2)

        # 添加自定义图例
        low_handle = Patch(color="#9dc1c5", label="较低")
        normal_handle = Patch(color="#8e93af", label="一般")
        high_handle = Patch(color="#d7a6b3", label="较高")
        handles = [low_handle, normal_handle, high_handle]
        ax.legend(handles=handles, loc="upper right", handleheight=1, handlelength=1, ncol=3)

        # 设置网格和背景色
        ax.grid(axis='y', linestyle='--', linewidth=1.5, color="#ffffff", zorder=1)
        yticks = ax.get_yticks()
        for i in range(len(yticks) - 1):
            if i % 2 == 1:  # 隔一行一种颜色
                ax.axhspan(yticks[i], yticks[i + 1], facecolor="#f6f8fb")

        ax.tick_params(axis="x", rotation=0)

        # 调整刻度字体大小
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        # 优化布局和保存图像
        plt.tight_layout()
        plt.savefig(self.workpath + r'\config\result.png', dpi=300, bbox_inches='tight')
        plt.close()