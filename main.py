from pathlib import Path

from plot import draw_dist_plot, draw_single, draw_scatter_plot
from stat_analyse import compare_num_people
from stat_analyse import run_stat_tasks_with_multiprocess, run_stat_tasks


def main():
    path_list = [path.absolute() for path in Path('./data').rglob("*_2025*.csv")]
    # path_list = [Path('./data/江西_2021_历史类.csv')]
    result = run_stat_tasks(path_list)
    # compare_num_people(result)
    # compare_phyhis_ratio(result)
    # compare_other_index(result)
    # draw_single(result[0], title="2021年 江西(文科)")
    draw_dist_plot(result)
    # draw_scatter_plot(result)
    # draw_scatter_plot(result)
    # compare_skewness(result)


if __name__ == "__main__":
    main()
