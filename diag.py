import pandas as pd
import numpy as np


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


def fuse_junior_undergraduate(csv_path: str):
    df = pd.read_csv(csv_path)
    num_people = df['num_people']
    accumulate = df['accumulate']
    accumulate = np.array(accumulate.to_numpy())
    num_people = np.array(num_people.to_numpy())
    
    for i in range(1, len(num_people)):
        accumulate[i] = accumulate[i-1] + num_people[i]
        
    df['accumulate'] = accumulate
    
    splits = csv_path.split('.')
    saved_path = splits[-2] + "_fused." + splits[-1]
    
    df.to_csv(saved_path, index=False)
