import math
from matplotlib.axes import Axes
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
plt.rcParams['font.family'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def bowley_skewness(data):
    q1 = np.percentile(data, 25, method='midpoint')
    q2 = np.percentile(data, 50, method='midpoint')
    q3 = np.percentile(data, 75, method='midpoint')
    s_q = (q3+q1-2*q2)/(q3-q1)
    return s_q


physics_data =[]
history_data = []
other_data = []

def run_stats(csv_path, province, ign_bound: bool):
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
    bowley_skew = bowley_skewness(full_data)
    kurt = stats.kurtosis(full_data, fisher=True, bias=False)
    var = full_data.var()
    mean = full_data.mean()

    print(csv_path)
    print(f'Mean: {mean}')
    print(f'Variance: {var}')
    print(f"Skew: {skew}")
    print(f"Kurtosis: {kurt}")

    data = {
        "province": province,
        "scores": scores,
        "num_people": num_people,
        "mean": mean,
        "standard": math.sqrt(var),
        "variance": var,
        "skewness": skew,
        "bowley_skewness": bowley_skew,
        "kurtosis": kurt
    }
    return data


def compare_skewness(data_list: list[dict]):
    data_list.sort(key=lambda x: x['bowley_skewness'])
    
    print("-----------")
    for i, data in enumerate(data_list):
        print(f"{i + 1}  {data['province']}  {data['bowley_skewness']}")


def main():

    ignore_bound = True
    provinces = ['黑龙江', '吉林', '辽宁', '内蒙古',
                 '河南', '河北', '山西', '陕西',
                 '宁夏', '青海', '湖北', '湖南',
                 '福建', '安徽', '江西', '江苏',
                 '四川', '重庆', '贵州', '云南',
                 '广东', '广西']

    def draw_provice(ax: Axes, title: str, data: dict, color: str):
        ax.bar(data['scores'], data['num_people'],
               width=1.0, color=color, edgecolor='none')
        ax.set_title(title)
        ax.set_xlim(0, 800)
        ax.tick_params(axis='both', labelsize=8)
        # ax.text(0, 0.7, f'平均值：{data['mean']:.2f}', transform=ax.transAxes)
        labels = [
            f'均值：{data['mean']:.2f}',
            f'标准差：{data['standard']:.2f}',
            f'偏度：P {data['skewness']:.2f}; B {data['bowley_skewness']:.2f}',
            f'峰度：{data['kurtosis']:.2f}',
        ]
        if data.get('description', None):
            labels.append(f'注：{data['description']}')

        label = "\n".join(labels)
        ax.set_xlabel(label, fontsize=8)

    axs_col = math.ceil(len(provinces) / 2)
    fig, axs = plt.subplots(5, axs_col, figsize=(16, 12))
    year = '2025'

    for i, p in enumerate(provinces):
        file_p = f'./data/{p}_{year}_物理类.csv'
        file_h = f'./data/{p}_{year}_历史类.csv'
        data_p = run_stats(file_p, f'{p}（物理类）', ignore_bound)
        physics_data.append(data_p)
        data_h = run_stats(file_h, f'{p}（历史类）', ignore_bound)
        history_data.append(data_h)

        draw_provice(axs[i // axs_col, i % axs_col],
                     f'{p}（物理类）', data_p, color='#1f77b4')
        draw_provice(axs[i // axs_col + 2, i % axs_col],
                     f'{p}（历史类）', data_h, color="#10910b")

    # 特殊地区
    data_beijing = run_stats(f'./data/北京_{year}.csv', '北京', ignore_bound)
    data_beijing['description'] = '379分以下由中位值拟合'
    draw_provice(axs[4, 0], f'北京', data_beijing, color="#ee6d17")
    provinces.append('北京')
    other_data.append(data_beijing)

    data_hainan = run_stats(f'./data/海南_{year}.csv', '海南', ignore_bound)
    data_hainan['description'] = '满分为800分'
    draw_provice(axs[4, 1], f'海南', data_hainan, color="#ee6d17")
    provinces.append('海南')
    other_data.append(data_hainan)

    data_shandong = run_stats(f'./data/山东_{year}.csv', '山东', ignore_bound)
    draw_provice(axs[4, 2], f'山东', data_shandong, color="#ee6d17")
    provinces.append('山东')
    other_data.append(data_shandong)

    data_zhejiang = run_stats(f'./data/浙江_{year}.csv', '浙江', ignore_bound)
    draw_provice(axs[4, 3], f'浙江', data_zhejiang, color="#ee6d17")
    provinces.append('浙江')
    other_data.append(data_zhejiang)

    data_tianjin = run_stats(f'./data/天津_{year}.csv', '天津', ignore_bound)
    draw_provice(axs[4, 4], f'天津', data_tianjin, color="#ee6d17")
    provinces.append('天津')
    other_data.append(data_tianjin)

    data_shanghai = run_stats(f'./data/上海_{year}.csv', '上海', ignore_bound)
    data_shanghai['description'] = '402分以下数据未公开'
    draw_provice(axs[4, 5], f'上海', data_shanghai, color="#ee6d17")
    provinces.append('上海')
    other_data.append(data_shanghai)

    fig.suptitle(
        f'{year}年部分省市高考成绩统计图\n注：本统计仅覆盖中国大陆实施新高考改革的省份。不含西藏（数据未公布）、新疆（传统高考模式）及港澳台地区（制度差异）。\n制作：赤川鹤鸣_Channel')
    plt.tight_layout()
    # plt.show()
    plt.savefig('figure.png', dpi=300, bbox_inches='tight')
    
    compare_skewness(physics_data)
    compare_skewness(history_data)
    compare_skewness(other_data)


if __name__ == "__main__":
    main()
