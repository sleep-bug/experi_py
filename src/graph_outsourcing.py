import matplotlib.pyplot as plt
import os
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 第一组数据 (ms 转换为 s)
x_values = [2000, 4000, 6000, 8000, 10000]
y_values = [91, 207, 364, 506, 971]         # 第一组运行时间 (ms)
y_values_seconds = [y / 1000 for y in y_values]  # 第一组转换为秒

# 第二组数据 (单位: 秒)
y_values_seconds_2 = [120, 254, 393, 569, 708]  # 第二组运行时间 (s)

# 第三组数据 (单位: 秒)
y_values_third_group = [25, 33.7, 40.5, 53.99, 72]  # 第三组运行时间 (s)

# 插值
extra_x = [3000, 5000, 7000, 9000]
extra_y_seconds = np.interp(extra_x, x_values, y_values_seconds)         # 第一组插值结果（秒）
extra_y_seconds_2 = np.interp(extra_x, x_values, y_values_seconds_2)     # 第二组插值结果
extra_y_third_group = np.interp(extra_x, x_values, y_values_third_group) # 第三组插值结果

# 创建保存路径
save_path = "E:\\experi\\output\\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 绘制折线图
fig, ax = plt.subplots(figsize=(5, 3))  # 设置为适合论文插入的大小

# 绘制第一条折线 (秒)
ax.plot(x_values, y_values_seconds, color='orange', linestyle='-', linewidth=2, label="SSPQ")
ax.scatter(x_values, y_values_seconds, color='orange', marker='D', s=50)
ax.scatter(extra_x, extra_y_seconds, color='orange', marker='D', s=50)  # 插值点标记

# 绘制第二条折线 (秒)
ax.plot(x_values, y_values_seconds_2, color='purple', linestyle='-', linewidth=2, label="PPSK+")
ax.scatter(x_values, y_values_seconds_2, color='purple', marker='D', s=50)
ax.scatter(extra_x, extra_y_seconds_2, color='purple', marker='D', s=50)  # 插值点标记

# 绘制第三条折线 (秒)
ax.plot(x_values, y_values_third_group, color='teal', linestyle='-', linewidth=2, label="[26]")
ax.scatter(x_values, y_values_third_group, color='teal', marker='D', s=50)
ax.scatter(extra_x, extra_y_third_group, color='teal', marker='D', s=50)  # 插值点标记

# 设置横坐标刻度
ax.set_xticks(x_values)
ax.set_xticklabels([str(x) for x in x_values])

# 添加标签
ax.set_xlabel("Number of Data Items", fontsize=12)
ax.set_ylabel("Outsourcing Time (s)", fontsize=12)  # 设置为秒

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.6)

# 添加图例
ax.legend(fontsize=10)

# 创建放大视图并调整位置
ax_inset = inset_axes(ax, width=1.3, height=0.8, loc="center right", bbox_to_anchor=(0.99, 0.38), bbox_transform=ax.transAxes)
ax_inset.plot(x_values, y_values_seconds, color='orange', linestyle='-', linewidth=2)
ax_inset.plot(x_values, y_values_third_group, color='teal', linestyle='-', linewidth=2)
ax_inset.scatter(x_values, y_values_seconds, color='orange', marker='D', s=50)
ax_inset.scatter(x_values, y_values_third_group, color='teal', marker='D', s=50)

# 设置放大视图的范围和 y 轴刻度
ax_inset.set_xlim(2000, 10000)
ax_inset.set_ylim(0, 1)
ax_inset.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])

# 隐藏放大视图的 x 轴标签
ax_inset.set_xticklabels([])

# 保存图表
output_path = os.path.join(save_path, "Outsourcing_chart_third_with.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 高分辨率保存，去除空白边距

print(f"折线图已保存至: {output_path}")
