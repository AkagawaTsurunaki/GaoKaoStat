import math
from pathlib import Path
from typing import List
from matplotlib.axes import Axes
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from plot import draw_distribute, draw_dist_plot, draw_scatter_plot
from stat_analyse import comapre_cvm, compare_other_index, compare_phyhis_ratio, compare_moment, group_by_subject_sort_by_province, run_stat_tasks, ScoreStat, run_stat_tasks_with_multiprocess
plt.rcParams['font.family'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def main():
    path_list = [path.absolute() for path in Path('./data').rglob("*.csv")]
    result = run_stat_tasks_with_multiprocess(path_list)
    comapre_cvm(result)
    # compare_phyhis_ratio(result)
    # compare_other_index(result)
    # draw_dist_plot(result)
    # draw_scatter_plot(result)
    # compare_skewness(result)


if __name__ == "__main__":
    main()
