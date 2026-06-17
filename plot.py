import math
import time
from typing import List

from matplotlib import pyplot as plt, ticker
from matplotlib.axes import Axes
import numpy as np
from adjustText import adjust_text

from stat_analyse import ScoreStat, group_by_subject_sort_by_province

# 默认用的是钉钉进步体，在这可以换成你自己的，NotoSans 字体有些奇怪但是也能看懂
plt.rcParams['font.family'] = ["DingTalk JinBuTi", 'SimHei', 'Noto Sans CJK JP', 'Noto Sans', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

COLOR_PHYSICS = "#0095ff"
COLOR_HISTORY = '#ff6600'
COLOR_OTHER = '#10910b'

def draw_distribute(ax: Axes, data: ScoreStat, color: str, show_score_lines: bool = False, title:str=None):
    ax.bar(data.scores, data.num_people,
           width=1.0, color=color, edgecolor='none')
    if not title:
        if data.subject:
            title = f'{data.province}({data.subject})'
        else:
            title = data.province
    ax.set_title(title)
    upper = 900 if data.province == '海南' else 750
    lower = 100 if data.province  == '海南' else 0
    ax.xaxis.set_major_locator(ticker.MultipleLocator(200))
    ax.set_xlim(lower, upper)
    ax.tick_params(axis='both', labelsize=8)
    if show_score_lines:
        if data.levelA and data.levelB:
            ax.axvline(data.levelA, color='red', linestyle='--',
                       linewidth=0.8)
            ax.axvline(data.levelB, color='blue', linestyle='--',
                       linewidth=0.8)
        ax.axvline(data.mean, color='orange', linestyle='--', linewidth=0.8)
    labels = [
        f'均值: {data.mean:.2f}',
        f'标准差: {data.standard:.2f}',
        f'偏度: P {data.skewness:.2f}; B {data.bowley_skewness:.2f}',
        f'峰度: {data.kurtosis:.2f}',
    ]
    if data.description:
        labels.append(f'注：{data.description}')

    label = "\n".join(labels)
    ax.set_xlabel(label, fontsize=8)

def draw_single(data: ScoreStat, title: str = None):
    fig, axs = plt.subplots(1, 1, figsize=(3, 3))
    draw_distribute(axs, data, COLOR_OTHER,title=title)
    plt.savefig(f'1.png', dpi=1200, bbox_inches='tight')
    plt.tight_layout()
    plt.close()

def draw_dist_plot(data_list: List[ScoreStat]):
    start = time.time()
    phy, his, other = group_by_subject_sort_by_province(data_list)
    # 3+1+2的省份很多, 因此整个子图横数量按照3+1+2省份来算个数, 分两行
    axs_col = math.ceil(len(phy) / 2)
    fig, axs = plt.subplots(5, axs_col, figsize=(16, 12))

    for i, (p, h) in enumerate(zip(phy, his)):
        draw_distribute(axs[i // axs_col, i % axs_col], p, color=COLOR_PHYSICS)
        draw_distribute(axs[i // axs_col + 2, i % axs_col], h, color=COLOR_HISTORY)

    for i, o in enumerate(other):
        draw_distribute(axs[-1, i], o, color=COLOR_OTHER)

    title = '2025年部分省市高考成绩统计图'
    fig.suptitle(
        f'{title}\n'
        '注：本统计仅覆盖中国大陆实施新高考改革的省份。不含西藏（数据未公布）、新疆（传统高考模式）及港澳台地区（制度差异）。\n'
        '制作：赤川鹤鸣_Channel')
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'{title}.png', dpi=1200, bbox_inches='tight')
    plt.close()
    end = time.time()
    print(f"Used {end - start:.2f} seconds")

# x軸是本科线-均值差，y軸是本科线-专科线
def draw_scatter_plot(data_list: List[ScoreStat]):
    fig, ax = plt.subplots(figsize=(8, 6))
    phy, his, other = group_by_subject_sort_by_province(data_list)
    point_size = 300

    x_arr_p, y_arr_p, s_arr_p = [], [], []
    for p in phy:
        assert p.levelA and p.levelB
        x = p.levelA - p.median
        x_arr_p.append(x)
        y = p.levelA - p.levelB
        y_arr_p.append(y)
        s_arr_p.append(p.total)

    s_arr_p = np.array(s_arr_p)
    factor = max(s_arr_p)
    s_arr_p = s_arr_p / factor * point_size
    ax.scatter(x_arr_p, y_arr_p, s_arr_p, color=COLOR_PHYSICS, label="物理类")
    ax.axvline(0,  color="#2e2e2e", linewidth=0.8)
    ax.set_xlabel('本科线与均值之差 (本科线 - 中位数)')
    ax.set_ylabel('本科线与专科线之差 (本科线 - 专科线)')

    x_arr_h, y_arr_h, s_arr_h = [], [], []
    for h in his:
        assert h.levelA and h.levelB
        x = h.levelA - h.median
        x_arr_h.append(x)
        y = h.levelA - h.levelB
        y_arr_h.append(y)
        s_arr_h.append(h.total)
    s_arr_h = np.array(s_arr_h)
    s_arr_h = s_arr_h / factor * point_size
    ax.scatter(x_arr_h, y_arr_h, s_arr_h, color=COLOR_HISTORY, label="历史类")
    offset = (1, 1)

    # 连接各省物理历史的那条线
    for i in range(len(phy)):
        ax.plot([x_arr_p[i], x_arr_h[i]], [y_arr_p[i], y_arr_h[i]],
                 color="#acacac", alpha=0.5, linewidth=0.8)

    # 物理/历史画圆点
    texts = []
    for i, p in enumerate(phy):
        texts.append(plt.text(x_arr_p[i], y_arr_p[i], p.province, fontsize=9))
    for i, h in enumerate(his):
        texts.append(plt.text(x_arr_h[i], y_arr_h[i], h.province, fontsize=9))
    adjust_text(
        texts,
        arrowprops=dict(arrowstyle="->", color="#3a3a3a", lw=0.5),
        expand_points=(0, 1.5),
        force_text=(0.8, 0.8),
        lim=1000
    )
    delta_y = np.array(y_arr_h) - np.array(y_arr_p) 
    delta_x = np.array(x_arr_h) - np.array(x_arr_p)
    xuefeng = delta_y / delta_x
    print([p.province for p in phy])
    print(xuefeng)
        
    ax.set_title('2025年部分省市高考本科线、专科线、中位数的偏离度分析——雪峰效应\n'
              '注: 气泡大小表示考生人数的多少; 横坐标表示本科线与平均值之间的区间有多大, 纵坐标表示本科线和专科线之间的区间有多大\n'
              '制作: 赤川鹤鸣_Channel')
    ax.legend()
    # plt.show()
    title = "2025年部分省市高考本科线、专科线、中位数的偏离度分析"
    plt.savefig(f'{title}.png', dpi=1200, bbox_inches='tight')
    plt.close()
