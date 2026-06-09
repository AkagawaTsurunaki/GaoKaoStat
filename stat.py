import math
from tkinter import font

from matplotlib.axes import Axes
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
plt.rcParams['font.family'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def run_stats(csv_path, ign_bound: bool):
    df = pd.read_csv(csv_path)

    scores = df['score']
    num_people = df['num_people']

    scores = np.array(scores.to_numpy())
    num_people = np.array(num_people.to_numpy())
    
    if ign_bound:
        scores = scores[1:-1]
        num_people = num_people[1:-1]

    # table = np.concat(scores, num_people)
    # table = np.column_stack([scores, num_people])

    full_data = np.repeat(scores, num_people)
    skew = stats.skew(full_data, bias=False)
    kurt = stats.kurtosis(full_data, fisher=True, bias=False)
    var = full_data.var()
    mean = full_data.mean()

    print(csv_path)
    print(f'Mean: {mean}')
    print(f'Variance: {var}')
    print(f"Skew: {skew}")
    print(f"Kurtosis: {kurt}")

    return {
        "scores": scores,
        "num_people": num_people,
        "mean": mean,
        "standard": math.sqrt(var),
        "variance": var,
        "skewness": skew,
        "kurtosis": kurt
    }


def main():

    ignore_bound = True
    provinces = ['辽宁', '河南', '河北', '湖北', '湖南', '四川', '广东', '广西'] # '江苏'

    def draw_provice(ax: Axes, title: str, data: dict):
        ax.bar(data['scores'], data['num_people'], width=1.0, color='#1f77b4', edgecolor='none')
        ax.set_title(title)
        ax.set_xlim(100, 700)
        # ax.text(0, 0.7, f'平均值：{data['mean']:.2f}', transform=ax.transAxes)
        labels = [
            f'均值：{data['mean']:.2f}',
            f'标准差：{data['standard']:.2f}',
            f'偏度：{data['skewness']:.2f}',
            f'峰度：{data['kurtosis']:.2f}',
        ]
        if data.get('description', None):
            labels.append(f'注：{data['description']}')
        
        label = "\n".join(labels)
        ax.set_xlabel(label)


    fig, axs = plt.subplots(2, len(provinces) + 1, figsize=(16, 6))
    year = '2025'
    
    for i, p in enumerate(provinces):
        file_p = f'./data/{p}_{year}_物理类.csv'
        file_h = f'./data/{p}_{year}_历史类.csv'
        data_p = run_stats(file_p, ignore_bound)
        data_h = run_stats(file_h, ignore_bound)
        draw_provice(axs[0, i], f'{p}（物理类）', data_p)
        draw_provice(axs[1, i], f'{p}（历史类）', data_h)

    # 特殊地区
    data_beijing = run_stats(f'./data/北京_{year}.csv', ignore_bound)
    data_beijing['description'] = '379分以下由中位值拟合'
    draw_provice(axs[0, -1], f'北京', data_beijing)
    provinces.append('北京')
    
    fig.suptitle(f'{year}年部分省市高考成绩统计图\n（{"、".join(provinces)}）\n制作：赤川鹤鸣_Channel')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
