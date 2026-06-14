from pathlib import Path

from plot import draw_dist_plot, draw_single
from stat_analyse import compare_num_people
from stat_analyse import run_stat_tasks_with_multiprocess


def main():
    # path_list = [path.absolute() for path in Path('./data').rglob("*_2025_*.csv")]
    path_list = [Path('./data/江西_2021_历史类.csv')]
    result = run_stat_tasks_with_multiprocess(path_list)
    # compare_num_people(result)
    # comapre_cvm(result)
    # compare_phyhis_ratio(result)
    # compare_other_index(result)
    draw_single(result[0])
    # draw_dist_plot(result)
    # draw_scatter_plot(result)
    # compare_skewness(result)


if __name__ == "__main__":
    main()
