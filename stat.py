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


physics_data = []
history_data = []
other_data = []


def run_stats(csv_path, province: str, subject: str = None, ign_bound: bool = True):
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
        "subject": subject,
        "scores": scores,
        "num_people": num_people,
        "total": int(np.sum(num_people)),
        "mean": mean,
        "standard": math.sqrt(var),
        "variance": var,
        "skewness": skew,
        "bowley_skewness": bowley_skew,
        "kurtosis": kurt
    }
    return data


def compare_skewness(data_list: list[dict]):
    data_list = data_list.copy()
    data_list.sort(key=lambda x: x['bowley_skewness'])

    print("-----各省市不同选科成绩分布偏度对比------")
    for i, data in enumerate(data_list):
        print(f"{i + 1}  {data['province']}  {data['bowley_skewness']}")


def compare_accumulate(physics: list[dict], history: list[dict], other: list[dict]):
    physics, history, other = physics.copy(), history.copy(), other.copy()
    result = []
    for p, h in zip(physics, history):
        assert p['province'] == h['province']
        total = p['total'] + h['total']
        result.append({
            "province": p['province'],
            "total": total
        })
    for o in other:
        result.append({
            "province": o['province'],
            "total": o['total']
        })
    result.sort(key=lambda x: x['total'], reverse=True)

    print("-----有效考生人数------")
    for i, data in enumerate(result):
        print(f"{i + 1}  {data['province']}  {data['total']}")


def compare_physics_history_ratio(physics: list[dict], history: list[dict]):
    physics, history = physics.copy(), history.copy()
    result = []
    for p, h in zip(physics, history):
        assert p['province'] == h['province']
        r = p['total'] / h['total']
        result.append({
            "province": p['province'],
            "ratio": r
        })

    result.sort(key=lambda x: x['ratio'], reverse=True)

    print('------物理/历史人数比------')
    for i, data in enumerate(result):
        print(f'{i+1} {data["province"]}  {data['ratio']}')


score_lines = {
    "黑龙江": {"历史类": {"本科线": 405, "专科线": 160}, "物理类": {"本科线": 360, "专科线": 160}},
    "陕西":   {"历史类": {"本科线": 414, "专科线": 200}, "物理类": {"本科线": 394, "专科线": 200}},
    "重庆":   {"历史类": {"本科线": 438, "专科线": 180}, "物理类": {"本科线": 425, "专科线": 180}},
    "辽宁":   {"历史类": {"本科线": 437, "专科线": 150}, "物理类": {"本科线": 367, "专科线": 150}},
    "福建":   {"历史类": {"本科线": 450, "专科线": 235}, "物理类": {"本科线": 441, "专科线": 235}},
    "湖南":   {"历史类": {"本科线": 446, "专科线": 200}, "物理类": {"本科线": 405, "专科线": 200}},
    "河南":   {"历史类": {"本科线": 471, "专科线": 185}, "物理类": {"本科线": 427, "专科线": 185}},
    "河北":   {"历史类": {"本科线": 477, "专科线": 200}, "物理类": {"本科线": 459, "专科线": 200}},
    "江西":   {"历史类": {"本科线": 486, "专科线": 290}, "物理类": {"本科线": 429, "专科线": 240}},
    "江苏":   {"历史类": {"本科线": 482, "专科线": 220}, "物理类": {"本科线": 463, "专科线": 220}},
    "广西":   {"历史类": {"本科线": 402, "专科线": 200}, "物理类": {"本科线": 370, "专科线": 200}},
    "广东":   {"历史类": {"本科线": 464, "专科线": 215}, "物理类": {"本科线": 436, "专科线": 200}},
    "山西":   {"历史类": {"本科线": 443, "专科线": 100}, "物理类": {"本科线": 419, "专科线": 100}},
    "安徽":   {"历史类": {"本科线": 477, "专科线": 200}, "物理类": {"本科线": 461, "专科线": 200}},
    "宁夏":   {"历史类": {"本科线": 404, "专科线": 150}, "物理类": {"本科线": 372, "专科线": 150}},
    "四川":   {"历史类": {"本科线": 467, "专科线": 150}, "物理类": {"本科线": 438, "专科线": 150}},
    "内蒙古": {"历史类": {"本科线": 418, "专科线": 160}, "物理类": {"本科线": 375, "专科线": 160}},
    "云南":   {"历史类": {"本科线": 465, "专科线": 180}, "物理类": {"本科线": 430, "专科线": 180}},
    "青海":   {"历史类": {"本科线": 405, "专科线": 150}, "物理类": {"本科线": 350, "专科线": 150}},
    "贵州":   {"历史类": {"本科线": 458, "专科线": 180}, "物理类": {"本科线": 387, "专科线": 180}},
    "湖北":   {"历史类": {"本科线": 442, "专科线": 200}, "物理类": {"本科线": 426, "专科线": 200}},
    "吉林":   {"历史类": {"本科线": 384, "专科线": 160}, "物理类": {"本科线": 340, "专科线": 160}},
}


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
        if data.get('levelA', None):
            ax.axvline(data['levelA'], color='red', linestyle='--',
                       linewidth=0.8)
            ax.axvline(data['levelB'], color='blue', linestyle='--',
                       linewidth=0.8)
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
        data_p = run_stats(file_p, province=p, subject="物理类",
                           ign_bound=ignore_bound)
        physics_data.append(data_p)
        data_h = run_stats(file_h, province=p, subject="历史类",
                           ign_bound=ignore_bound)
        history_data.append(data_h)

        data_p['levelA'] = score_lines[p]['物理类']['本科线']
        data_p['levelB'] = score_lines[p]['物理类']['专科线']
        draw_provice(axs[i // axs_col, i % axs_col],
                     f'{p}（物理类）', data_p, color='#1f77b4')
        data_h['levelA'] = score_lines[p]['历史类']['本科线']
        data_h['levelB'] = score_lines[p]['历史类']['专科线']
        draw_provice(axs[i // axs_col + 2, i % axs_col],
                     f'{p}（历史类）', data_h, color="#10910b")

    # 特殊地区
    data_beijing = run_stats(
        f'./data/北京_{year}.csv', province='北京', ign_bound=ignore_bound)
    data_beijing['description'] = '379分以下由中位值拟合'
    draw_provice(axs[4, 0], f'北京', data_beijing, color="#ee6d17")
    provinces.append('北京')
    other_data.append(data_beijing)

    data_hainan = run_stats(
        f'./data/海南_{year}.csv', '海南', ign_bound=ignore_bound)
    data_hainan['description'] = '满分为800分'
    draw_provice(axs[4, 1], f'海南', data_hainan, color="#ee6d17")
    provinces.append('海南')
    other_data.append(data_hainan)

    data_shandong = run_stats(
        f'./data/山东_{year}.csv', '山东', ign_bound=ignore_bound)
    draw_provice(axs[4, 2], f'山东', data_shandong, color="#ee6d17")
    provinces.append('山东')
    other_data.append(data_shandong)

    data_zhejiang = run_stats(
        f'./data/浙江_{year}.csv', '浙江', ign_bound=ignore_bound)
    draw_provice(axs[4, 3], f'浙江', data_zhejiang, color="#ee6d17")
    provinces.append('浙江')
    other_data.append(data_zhejiang)

    data_tianjin = run_stats(
        f'./data/天津_{year}.csv', '天津', ign_bound=ignore_bound)
    draw_provice(axs[4, 4], f'天津', data_tianjin, color="#ee6d17")
    provinces.append('天津')
    other_data.append(data_tianjin)

    data_shanghai = run_stats(
        f'./data/上海_{year}.csv', '上海', ign_bound=ignore_bound)
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

    compare_accumulate(physics_data, history_data, other_data)

    compare_physics_history_ratio(physics_data, history_data)


if __name__ == "__main__":
    main()
