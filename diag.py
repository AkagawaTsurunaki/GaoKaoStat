import os

import pandas as pd
import numpy as np


def sync_num_people_by_accum(csv_path):
    df = pd.read_csv(csv_path)

    diff = get_num_people_from_accum(df)

    df['num_people'] = diff
    saved_path = rename(csv_path)
    df.to_csv(saved_path, index=False)

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

    saved_path = rename(csv_path)
    df.to_csv(saved_path, index=False)


def rename(path: str):
    splits = path.split('.')
    new_path = splits[-2] + "_fused." + splits[-1]
    return new_path


def get_num_people_from_accum(df):
    accumulate = df['accumulate']
    accumulate = np.array(accumulate.to_numpy())
    accumulate = np.concat([[0], accumulate])

    diff = np.diff(accumulate, 1)
    assert np.sum(diff) == accumulate[-1]
    return diff


def validate_data(csv_path: str):
    assert os.path.exists(csv_path), f'Path does not exist: {csv_path}'
    df = pd.read_csv(csv_path)
    num_people = np.array(df['num_people'].to_numpy())
    diff = get_num_people_from_accum(df)
    
    count = 0
    err = 0
    
    for i in range(len(num_people)):
        if diff[i] != num_people[i]:
            print(f"At index {i}, inconsistency num_people ({num_people[i]}) should be {diff[i]} from accumulate.")
            err += 1
        if num_people[i] < 0 or diff[i] < 0:
            print(f"At index {i}, num_people < 0.")
            err += 1
        count += 1
    
    print(f"Validation: {count} row(s) are checked.")
    if err == 0:
        print(f'No problem.')
    else:
        print(f"{err} error(s) need to fix.")
        

path = R'.\data\天津_2025.csv'
# validate_data(path)
# sync_num_people_by_accum(path)
validate_data(path)
