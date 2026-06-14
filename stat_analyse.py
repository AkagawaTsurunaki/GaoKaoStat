import concurrent
import concurrent.futures
from dataclasses import dataclass
import math
import multiprocessing
from pathlib import Path
import time
from typing import List, Tuple, Union
import pandas as pd
import numpy as np
from scipy import stats

from extra_info import DESCRIPTION, SCORE_LINE


@dataclass()
class ScoreStat:
    year: int
    province: str
    subject: str | None
    scores: np.ndarray
    num_people: np.ndarray
    total: int
    mean: float
    median: float
    standard: float
    variance: float
    skewness: float
    bowley_skewness: float
    kurtosis: float
    abci: int  # 本人提出的“绝对独木桥指标”/“一分千人指标”，提高一分，干掉千人，即一分一段表中超过1000人的分数线有多少个。
    bci: int
    cvm: float  # Cramér–von Mises 统计量，不用 Anderson–Darling 因为它的权重在尾部很敏感
    cvm_p_value: float  # 这个统计量的 p 值，用于假设检验的
    levelA: int | None
    levelB: int | None
    description: str | None


def cramer_von_mises_statistic(data: np.ndarray, lower=0, upper=750):
    # rng = np.random.default_rng()
    # if data.size > 50_000:
    #     data = rng.choice(data, size=50_000, replace=False)
    #
    # loc_hat = np.mean(data)
    # scale_hat = np.std(data, ddof=1)
    #
    # a = (lower - loc_hat) / scale_hat
    # b = (upper - loc_hat) / scale_hat
    #
    # result = stats.goodness_of_fit(
    #     dist=stats.truncnorm,
    #     data=data,
    #     statistic='cvm',
    #     n_mc_samples=999,          # 999 次模拟已足够稳定，显著提速
    #     known_params={'a': a, 'b': b},  # 截尾点固定，只估计 loc/scale
    # )
    return 0, 0


def bowley_skewness(data):
    q1 = np.percentile(data, 25, method='midpoint')
    q2 = np.percentile(data, 50, method='midpoint')
    q3 = np.percentile(data, 75, method='midpoint')
    s_q = (q3 + q1 - 2 * q2) / (q3 - q1)
    return s_q


def run_stats(csv_path: Union[Path, str], ign_bound: bool = True):
    print(f"Processing: {csv_path}")
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)
    scores = np.array(df['score'].to_numpy())
    num_people = np.array(df['num_people'].to_numpy())
    accumulate = np.array(df['accumulate'].to_numpy())

    if ign_bound:
        scores = scores[1:-1]
        num_people = num_people[1:-1]

    total = int(accumulate[-1])
    full_data = np.repeat(scores, num_people)
    skew = stats.skew(full_data, bias=False)
    bowley_skew = bowley_skewness(full_data)
    kurt = stats.kurtosis(full_data, fisher=True, bias=False)
    var = full_data.var()
    mean = full_data.mean()
    median = np.median(full_data)
    abci = np.count_nonzero(num_people >= 1000)
    bci = np.count_nonzero(num_people >= total * 0.001)

    splits = csv_path.stem.split("_")
    province, year = splits[0], int(splits[1])
    subject = splits[2] if len(splits) >= 3 else None

    # 上海高考 (0~660)，海南高考 (100~900)
    if province == '上海':
        lower, upper = 0, 660
    elif province == '海南':
        lower, upper = 100, 900
    else:
        lower, upper = 0, 750
    # cvm = cramer_von_mises_statistic(full_data,lower, upper)

    # 某些省份不分文理科，本科线专科线
    score_lines = SCORE_LINE
    levelA = score_lines[province][subject]['本科线'] if province in score_lines.keys(
    ) else None
    levelB = score_lines[province][subject]['专科线'] if province in score_lines.keys(
    ) else None

    # 对数据的额外描述注释
    desc = DESCRIPTION.get(province, None)

    print(f"Data analysis completed: {csv_path}")

    return ScoreStat(
        year=year,
        province=province,
        subject=subject,
        levelA=levelA,
        levelB=levelB,
        scores=scores,
        num_people=num_people,
        total=total,
        mean=mean,
        median=median,
        standard=math.sqrt(var),
        variance=var,
        skewness=skew,
        bowley_skewness=bowley_skew,
        kurtosis=kurt,
        abci=int(abci),
        bci=int(bci),
        cvm=0,
        cvm_p_value=0,
        description=desc
    )


def group_by_subject_sort_by_province(stat_list: List[ScoreStat]) -> Tuple[
    List[ScoreStat], List[ScoreStat], List[ScoreStat]]:
    phy, his, other = [], [], []
    for data in stat_list:
        if data.subject == "物理类":
            phy.append(data)
        elif data.subject == "历史类":
            his.append(data)
        else:
            # 可能不是 3+1+2 的省份
            other.append(data)
    phy.sort(key=lambda x: x.province, reverse=False)
    his.sort(key=lambda x: x.province, reverse=False)
    return phy, his, other


def compare_num_people(stat_list: List[ScoreStat]):
    phy, his, other = group_by_subject_sort_by_province(stat_list)

    result = []
    for p, h in zip(phy, his):
        assert p.province == h.province
        r = p.total / h.total
        result.append({
            "province": p.province,
            "ratio": r,
            'delta': p.total - h.total
        })

    result.sort(key=lambda x: x['ratio'], reverse=True)

    print('------物理/历史人数比------')
    for i, data in enumerate(result):
        print(f'{i + 1} {data["province"]}  {data['ratio']}')

    sum_delta = sum([r['delta'] for r in result])
    print(f"总多出: {sum_delta}")

    phy = sorted(phy, key=lambda x: x.total, reverse=True)
    his = sorted(his, key=lambda x: x.total, reverse=True)
    other = sorted(other, key=lambda x: x.total, reverse=True)

    print('------物理人数------')
    for i, data in enumerate(phy):
        print(f'{i + 1} {data.province} {data.total}')

    print('------历史人数------')
    for i, data in enumerate(his):
        print(f'{i + 1} {data.province} {data.total}')
    print('------其他人数------')
    for i, data in enumerate(other):
        print(f'{i + 1} {data.province} {data.total}')

    total = sum([data.total for data in stat_list])
    print(f'所有省市的总人数：{total}')

def compare_other_index(stat_list: List[ScoreStat]):
    phy, his, _ = group_by_subject_sort_by_province(stat_list)

    phy_bci = sorted(
        phy,
        key=lambda s: s.abci,
        reverse=True
    )
    his_bci = sorted(
        his,
        key=lambda s: s.abci,
        reverse=True
    )

    print(R'------绝对“一分千人”指标排行（物理类）------')
    for i, data in enumerate(phy_bci):
        print(f'{i + 1} {data.province}  {data.abci} {data.total}')
    print(R'------绝对“一分千人”指标排行（历史类）------')
    for i, data in enumerate(his_bci):
        print(f'{i + 1} {data.province}  {data.abci} {data.total}')

    phy_bci = sorted(
        phy,
        key=lambda s: s.bci,
        reverse=True
    )
    his_bci = sorted(
        his,
        key=lambda s: s.bci,
        reverse=True
    )

    print('------0.1% “一分千人”指标排行（物理类）------')
    for i, data in enumerate(phy_bci):
        print(f'{i + 1} {data.province}  {data.bci}')
    print('------0.1% “一分千人”桥指标排行（历史类）------')
    for i, data in enumerate(his_bci):
        print(f'{i + 1} {data.province}  {data.bci}')


def compare_moment(stat_list: List[ScoreStat]):
    phy, his, _ = group_by_subject_sort_by_province(stat_list)

    # 按照平均值排序
    phy_mean = sorted(phy, key=lambda s: s.mean, reverse=True)
    his_mean = sorted(phy, key=lambda s: s.mean, reverse=True)
    print('------均值排行（物理类）------')
    for i, data in enumerate(phy_mean):
        print(f'{i + 1} {data.province}  {data.mean:.4f}')

    print('\n------均值排行（历史类）------')
    for i, data in enumerate(his_mean):
        print(f'{i + 1} {data.province}  {data.mean:.4f}')

    # 按普通偏度排序
    phy_std = sorted(phy, key=lambda s: s.standard, reverse=True)
    his_std = sorted(his, key=lambda s: s.standard, reverse=True)

    print('------标准差排行（物理类）------')
    for i, data in enumerate(phy_std):
        print(f'{i + 1} {data.province}  {data.standard:.4f}')

    print('\n------标准差排行（历史类）------')
    for i, data in enumerate(his_std):
        print(f'{i + 1} {data.province}  {data.standard:.4f}')

    # 按普通偏度排序
    phy_skew = sorted(phy, key=lambda s: s.skewness, reverse=False)
    his_skew = sorted(his, key=lambda s: s.skewness, reverse=False)

    print('------普通偏度排行（物理类）------')
    for i, data in enumerate(phy_skew):
        print(f'{i + 1} {data.province}  {data.skewness:.4f}')

    print('\n------普通偏度排行（历史类）------')
    for i, data in enumerate(his_skew):
        print(f'{i + 1} {data.province}  {data.skewness:.4f}')

    # 按鲍利偏度排序
    phy_bowley = sorted(phy, key=lambda s: s.bowley_skewness, reverse=False)
    his_bowley = sorted(his, key=lambda s: s.bowley_skewness, reverse=False)

    print('\n------鲍利偏度排行（物理类）------')
    for i, data in enumerate(phy_bowley):
        print(f'{i + 1} {data.province}  {data.bowley_skewness:.4f}')

    print('\n------鲍利偏度排行（历史类）------')
    for i, data in enumerate(his_bowley):
        print(f'{i + 1} {data.province}  {data.bowley_skewness:.4f}')

    # 按峰度排序
    phy_kurt = sorted(phy, key=lambda s: s.kurtosis, reverse=True)
    his_kurt = sorted(his, key=lambda s: s.kurtosis, reverse=True)

    print('\n------峰度排行（物理类）------')
    for i, data in enumerate(phy_kurt):
        print(f'{i + 1} {data.province}  {data.kurtosis:.4f}')

    print('\n------峰度排行（历史类）------')
    for i, data in enumerate(his_kurt):
        print(f'{i + 1} {data.province}  {data.kurtosis:.4f}')


def comapre_cvm(stat_list: List[ScoreStat]):
    phy, his, other = group_by_subject_sort_by_province(stat_list)

    phy = sorted(phy, key=lambda s: s.cvm_p_value, reverse=True)
    his = sorted(his, key=lambda s: s.cvm_p_value, reverse=True)
    other = sorted(other, key=lambda s: s.cvm_p_value, reverse=True)

    for i, data in enumerate(phy):
        print(
            f'{i + 1} {data.province}  cvm={data.cvm:.4f} p_value={data.cvm_p_value:.4f}')

    for i, data in enumerate(his):
        print(
            f'{i + 1} {data.province}  cvm={data.cvm:.4f} p_value={data.cvm_p_value:.4f}')

    for i, data in enumerate(other):
        print(
            f'{i + 1} {data.province}  cvm={data.cvm:.4f} p_value={data.cvm_p_value:.4f}')


def run_stat_tasks(path_list: List[Path]):
    result = []
    start = time.time()
    for path in path_list:
        data = run_stats(path)
        result.append(data)
    end = time.time()
    print(f"Use {end - start:.2f} seconds")
    return result


def run_stat_tasks_with_multiprocess(path_list: List[Path]):
    start = time.time()
    args = [str(path) for path in path_list]
    with concurrent.futures.ProcessPoolExecutor(10) as pool:
        result = list(pool.map(run_stats, args))
        end = time.time()
        print(f"Use {end - start:.2f} seconds")
        return result
