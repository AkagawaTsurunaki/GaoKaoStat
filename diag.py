import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def gen_num_people_by_accum(csv_path):
    df = pd.read_csv(csv_path)

    accumulate = df['accumulate']
    accumulate = np.array(accumulate.to_numpy())
    accumulate = np.concat([[0], accumulate])

    diff = np.diff(accumulate, 1)

    assert np.sum(diff) == accumulate[-1]
    df['num_people'] = diff
    df.to_csv(csv_path, index=False)

    print('Sync num_people based on accumulate column.')

gen_num_people_by_accum('./data/henan_2025_physics_scores.csv')
