from pathlib import Path

from plot import draw_dist_plot, draw_single, draw_scatter_plot
from stat_analyse import compare_moment, compare_num_people, compare_other_index
from stat_analyse import run_stat_tasks_with_multiprocess, run_stat_tasks


def main():
    path_list = [path.absolute() for path in Path('./data').rglob("*_2025*.csv")]
    result = run_stat_tasks(path_list)
    # result = run_stat_tasks_with_multiprocess(path_list)
    
    # 这些是直接在命令行输出的
    compare_num_people(result)
    compare_other_index(result)
    compare_moment(result)
    
    # 带 draw 开头的是画图的函数
    draw_dist_plot(result)
    draw_scatter_plot(result)

    # 想只输出某个省市的就用下面这个
    # path_list = [Path('./data/江西_2021_历史类.csv')]
    # draw_single(result[0], title="2021年 江西(文科)")
    
    print('Done')

if __name__ == "__main__":
    main()
