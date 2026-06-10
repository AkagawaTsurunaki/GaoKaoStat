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
    df = pd.read_csv(csv_path)
    num_people = np.array(df['num_people'].to_numpy())
    diff = get_num_people_from_accum(df)
    
    count = 0
    
    for i in range(len(num_people)):
        if diff[i] != num_people[i]:
            print(f"At index {i}, inconsistency num_people ({num_people[i]}) should be {diff[i]} from accumulate.")
        
        count += 1
    
    print(f"Validation success: {count} row(s) are checked.")
        

path = R'C:\Users\96514\Desktop\GaoKaoStat\data\宁夏_2025_历史类.txt'
# validate_data(path)
sync_num_people_by_accum(path)
validate_data(path)
