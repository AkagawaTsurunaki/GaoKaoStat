from dataclasses import dataclass
import math
from pathlib import Path
import time
from typing import List, Tuple
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
    standard: float
    variance: float
    skewness: float
    bowley_skewness: float
    kurtosis: float
    abci: int  # 本人提出的“绝对独木桥指标”/“一分千人指标”，提高一分，干掉千人，即一分一段表中超过1000人的分数线有多少个。
    bci: int
    levelA: int | None
    levelB: int | None
    description: str | None


def bowley_skewness(data):
    q1 = np.percentile(data, 25, method='midpoint')
    q2 = np.percentile(data, 50, method='midpoint')
    q3 = np.percentile(data, 75, method='midpoint')
    s_q = (q3+q1-2*q2)/(q3-q1)
    return s_q


def run_stats(csv_path: Path, ign_bound: bool = True):
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
    abci = np.count_nonzero(num_people >= 1000)
    bci = np.count_nonzero(num_people >= total * 0.001)

    splits = csv_path.stem.split("_")
    province, year = splits[0], int(splits[1])
    subject = splits[2]if len(splits) >= 3 else None

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
        standard=math.sqrt(var),
        variance=var,
        skewness=skew,
        bowley_skewness=bowley_skew,
        kurtosis=kurt,
        abci=int(abci),
        bci=int(bci),
        description=desc
    )


def group_by_subject_sort_by_province(stat_list: List[ScoreStat]) -> Tuple[List[ScoreStat], List[ScoreStat], List[ScoreStat]]:
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


def compare_phyhis_ratio(stat_list: List[ScoreStat]):
    phy, his, _ = group_by_subject_sort_by_province(stat_list)
    print([p.province for p in phy])
    print([p.province for p in his])

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
        print(f'{i+1} {data["province"]}  {data['ratio']}')

    sum_delta = sum([r['delta'] for r in result]) 
    print(f"总多出: {sum_delta}")


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

    print(R'------绝对独木桥指标排行（物理类）------')
    for i, data in enumerate(phy_bci):
        print(f'{i+1} {data.province}  {data.abci} {data.total}')
    print(R'------绝对独木桥指标排行（历史类）------')
    for i, data in enumerate(his_bci):
        print(f'{i+1} {data.province}  {data.abci} {data.total}')

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

    print('------0.1% 相对独木桥指标排行（物理类）------')
    for i, data in enumerate(phy_bci):
        print(f'{i+1} {data.province}  {data.bci}')
    print('------0.1% 相对独木桥指标排行（历史类）------')
    for i, data in enumerate(his_bci):
        print(f'{i+1} {data.province}  {data.bci}')


def run_stat_tasks(path_list: List[Path]):
    result = []
    start = time.time()
    for path in path_list:
        data = run_stats(path)
        result.append(data)
    end = time.time()
    print(f"Use {end - start:.2f} seconds")
    return result
