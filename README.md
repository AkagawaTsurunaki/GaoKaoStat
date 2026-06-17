# GaoKaoStat 高考成绩统计分析

对中国部分省市高考成绩数据的一些分析，包含程序源代码和高考数据。

分析内容包括，总人数、物理/历史考生占比，平均数、方差、偏度、峰度等，并以统计图和散点图的形式呈现。

你可以运行程序自己生成，也可以直接用我们生成好的图片，引用时请标明原作者。

原视频详见[赤川鹤鸣_Channel - 你考不过我你信不信？😰统计学告诉你高考成绩的真相](https://www.bilibili.com/video/BV19AjV6iE9w)

## 历年数据

### 2025 年

![img](./output/2025年部分省市高考成绩统计图.png)

注：图中偏度后面的 P 表示 Pearson 偏度，B 表示 Bowley 偏度，Bowley 偏度是根据分位数算的，对尾部敏感性比 Pearson 偏度低一些。

由于大部分省市的统计数据在某一个分数段之后就被截断了（例如100分以下），因此我们如实地阐述哪些地区的成绩数据是截尾分布。截尾分布对峰度和偏度都有一定影响。

带截尾：黑龙江、陕西、重庆、辽宁、福建、湖南、浙江、海南、河南、河北、江西、江苏、广西、广东、山西、山东、安徽、宁夏、天津、四川、北京、内蒙古、云南。

无截尾：青海、贵州、湖北、吉林、上海。

![img](./output/2025年部分省市高考本科线、专科线、中位数的偏离度分析.png)

## 使用说明

以下是从源代码和数据生成图表的流程，如果你不需要可以跳过此节。

假设你已经安装了 uv，运行下列命令安装项目的依赖：

```
uv sync
```

生成图表和排行数据，则运行：

```
uv run main.py
```

看到 `Done` 出现则完成。

## 引用我们

引用本视频

```
@misc{bilibili,
  author = {赤川鹤鸣_Channel},
  title = {你考不过我你信不信？😰统计学告诉你高考成绩的真相},
  year = {2026},
  month = {jun},
  url = {https://www.bilibili.com/video/BV19AjV6iE9w},
  howpublished = {Online video},
  note = {Accessed: 2026-06-17}
}
```

引用本仓库

```
@software{GaoKaoStat,
  author = {AkagawaTsurunaki},
  title = {GaoKaoStat 高考成绩统计分析},
  year = {2026},
  month = {jun},
  url = {https://github.com/AkagawaTsurunaki/GaoKaoStat},
  version = {0.1.0}
}
```
