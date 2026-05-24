import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
    skew_with_bias = stats.skew(full_data, bias=True)
    kurt = stats.kurtosis(full_data, fisher=False, bias=False)
    kurt_with_bias = stats.kurtosis(full_data, fisher=False, bias=True)

    print(csv_path)
    print(f"Skew: {skew} ({skew_with_bias})")
    print(f"Kurtosis: {kurt} ({kurt_with_bias})")
    
    return full_data

def main():
    ke = 'physics'
    ln_data = run_stats(f'./data/liaoning_2025_{ke}_scores.csv')
    hn_data = run_stats(f'./data/henan_2025_{ke}_scores.csv')

    plt.hist([ln_data, hn_data], bins=100)
    plt.show()

if __name__ == "__main__":
    main()
    

