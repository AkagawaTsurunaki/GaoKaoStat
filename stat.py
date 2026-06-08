import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
plt.rcParams['font.family'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def run_stats(csv_path):
    df = pd.read_csv(csv_path)

    scores = df['score']
    num_people = df['num_people']

    scores = np.array(scores.to_numpy())
    num_people = np.array(num_people.to_numpy())

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
        "variance": var,
        "skewness": skew,
        "kurtosis": kurt
    }


def main():

    provinces = ['辽宁', '河南', '河北', '四川', '江苏', '广东']

    def draw_provice(ax, title: str, data):
        ax.bar(data['scores'], data['num_people'], width=1.0, color='#1f77b4', edgecolor='none')
        ax.set_title(title)
        ax.set_xlim(100, 700)


    fig, axs = plt.subplots(2, len(provinces), figsize=(16, 6))
    
    for i, p in enumerate(provinces):
        file_p = f'./data/{p}_2025_物理类.csv'
        file_h = f'./data/{p}_2025_历史类.csv'
        data_p = run_stats(file_p)
        data_h = run_stats(file_h)
        draw_provice(axs[0, i], f'{p}（物理类）', data_p)
        draw_provice(axs[1, i], f'{p}（历史类）', data_h)


    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
