import matplotlib.pyplot as plt
import os
import numpy as np

# 第一组数据
x_values = [2000, 4000, 6000, 8000, 10000]  # 数据量
y_values = [16103, 22755, 49642, 65362, 98482]  # 第一组运行时间 (ms)

# 将第一组 y 值转换为秒
y_values_in_seconds = [y / 1000 for y in y_values]  # 转换为秒

# 第二组数据 (单位: 秒)
y_values_second_group = [16.8, 22, 23, 25, 29]  # 第二组运行时间 (s)

# 第三组数据 [25]，单位: 秒
y_values_third_group = [18, 38, 69, 95, 118]

# 插值
extra_x = [3000, 5000, 7000, 9000]
extra_y_in_seconds_first = np.interp(extra_x, x_values, y_values_in_seconds)  # 第一组插值结果
extra_y_in_seconds_second = np.interp(extra_x, x_values, y_values_second_group)  # 第二组插值结果
extra_y_in_seconds_third = np.interp(extra_x, x_values, y_values_third_group)  # 第三组插值结果

# 创建保存路径
save_path = r"E:\experi\output\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 绘制折线图
fig, ax = plt.subplots(figsize=(5, 3))  # 适合论文的图像尺寸

# 绘制第一条折线 (s)
ax.plot(x_values, y_values_in_seconds, color='orange', linestyle='-', linewidth=2, label="SSPQ")
ax.scatter(x_values + extra_x, y_values_in_seconds + list(extra_y_in_seconds_first), color='orange', marker='D', s=50)

# 绘制第二条折线 (s)
ax.plot(x_values, y_values_second_group, color='purple', linestyle='-', linewidth=2, label="PPSK+")
ax.scatter(x_values + extra_x, y_values_second_group + list(extra_y_in_seconds_second), color='purple', marker='D', s=50)

# 绘制第三条折线 [1] (s)
ax.plot(x_values, y_values_third_group, color='teal', linestyle='-', linewidth=2, label="[26]")
ax.scatter(x_values + extra_x, y_values_third_group + list(extra_y_in_seconds_third), color='teal', marker='D', s=50)

# 设置横坐标刻度，仅显示主要数据点
ax.set_xticks(x_values)
ax.set_xticklabels([str(x) for x in x_values])

# 添加标签
ax.set_xlabel("Number of Data Items", fontsize=12)
ax.set_ylabel("Search Time (s)", fontsize=12)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.6)

# 添加图例
ax.legend(fontsize=10)

# 保存图表
output_path = os.path.join(save_path, "Search_chart_third.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 高分辨率保存

print(f"折线图已保存至: {output_path}")
