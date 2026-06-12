from dataclasses import dataclass
import math
from pathlib import Path
import time
from typing import List
import pandas as pd
import numpy as np
from scipy import stats


@dataclass
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

    full_data = np.repeat(scores, num_people)
    skew = stats.skew(full_data, bias=False)
    bowley_skew = bowley_skewness(full_data)
    kurt = stats.kurtosis(full_data, fisher=True, bias=False)
    var = full_data.var()
    mean = full_data.mean()

    splits = csv_path.stem.split("_")
    province, year = splits[0], int(splits[1])
    subject = splits[2]if len(splits) >= 3 else None

    print(f"Data analysis completed: {csv_path}")

    return ScoreStat(
        year=year,
        province=province,
        subject=subject,
        scores=scores,
        num_people=num_people,
        total=int(accumulate[-1]),
        mean=mean,
        standard=math.sqrt(var),
        variance=var,
        skewness=skew,
        bowley_skewness=bowley_skew,
        kurtosis=kurt
    )


def run_stat_tasks(path_list: List[Path]):
    result = []
    start = time.time()
    for path in path_list:
        data = run_stats(path)
        result.append(data)
    end = time.time()
    print(f"Use {end - start:.2f} seconds")
    return result


if __name__ == "__main__":
    path_list = [path.absolute() for path in Path('./data').rglob("*.csv")]
    result = run_stat_tasks(path_list)
