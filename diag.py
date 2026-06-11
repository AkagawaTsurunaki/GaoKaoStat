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
    accumulate = np.array(accumulate, dtype=int)
    accumulate = np.concat([[0], accumulate])

    diff = np.diff(accumulate, 1)
    total = np.sum(diff)
    assert total == accumulate[-1], f'np.sum(diff) = {total}, while accumulate[-1] = {accumulate[-1]}'
    return diff


def validate_data(csv_path: str) -> bool:
    assert os.path.exists(csv_path), f'Path does not exist: {csv_path}'
    df = pd.read_csv(csv_path)
    num_people = np.array(df['num_people'].to_numpy(), dtype=int)
    scores = np.array(df['score'].to_numpy(), dtype=int)
    diff = get_num_people_from_accum(df)
    
    if np.isnan(num_people.any()):
        print("num_people has nan value.")
        return False
    if np.isnan(scores.any()):
        print("scores has nan value.")
        return False
    if np.isnan(diff.any()):
        print("diff has nan value.")
        return False
    count = 0
    err = 0
    
    for i in range(len(num_people)):
        if diff[i] != num_people[i]:
            print(f"At score {scores[i]}, inconsistency num_people ({num_people[i]}) should be {diff[i]} from accumulate.")
            err += 1
        if num_people[i] < 0 or diff[i] < 0:
            print(f"At index {i}, num_people < 0.")
            err += 1
        count += 1
    
    print(f"Validation: {count} row(s) are checked.")
    if err == 0:
        print(f'No problem.')
        return True
    else:
        print(f"{err} error(s) need to fix.")
        return False
        
for dirpath, dirnames, filenames in os.walk('./data'):
    for filename in filenames:
        if filename.split('.')[-1].lower() == 'csv':
            print("--------------")
            path = os.path.join(dirpath, filename)
            if not validate_data(path):
                print(f'Path: {path}')
                exit()
            else:
                print(f"Path: {path}")
            print("--------------")
# path = R'.\data\江苏_2025_历史类.csv'
# validate_data(path)
# sync_num_people_by_accum(path)
# validate_data(path)
