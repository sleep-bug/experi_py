import matplotlib.pyplot as plt
import os
import numpy as np

# 数据
x_values = [2000, 4000, 6000, 8000, 10000]  # 数据量
y_values = [24867, 48000, 66357, 93575, 139209]  # 运行时间 (ms)

# 将 y 值转换为秒
y_values_in_seconds = [y / 1000 for y in y_values]  # 转换为秒

# 要插值的点
extra_x = [3000, 5000, 7000, 9000]
extra_y_in_seconds = np.interp(extra_x, x_values, y_values_in_seconds)  # 插值结果

# 创建保存路径
save_path = "E:\\experi\\output\\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 绘制折线图
plt.figure(figsize=(5, 3))  # 适合论文插入的大小
plt.plot(x_values, y_values_in_seconds, color='orange', linestyle='-', linewidth=2)  # 绘制折线

# 添加原始数据点和插值点的菱形标记
plt.scatter(x_values, y_values_in_seconds, color='orange', marker='D', s=50)  # 原始点
plt.scatter(extra_x, extra_y_in_seconds, color='orange', marker='D', s=50)  # 插值点

# 添加标签
plt.xlabel("Number of Data Items", fontsize=12)
plt.ylabel("Data Recovery Time (s)", fontsize=12)

# 设置横坐标的刻度，仅显示原始数据点的数字
plt.gca().set_xticks([2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])  # 包括插值点的位置
plt.gca().set_xticklabels([2000, '', 4000, '', 6000, '', 8000, '', 10000])

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图表
output_path = os.path.join(save_path, "Recovery_chart.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 高分辨率保存，去除空白边距

print(f"折线图已保存至: {output_path}")
