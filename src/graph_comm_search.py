import matplotlib.pyplot as plt
import numpy as np
import os

# 原始数据
x_values = [2000, 4000, 6000, 8000, 10000]  # 数据量
y_values_first = [495.26, 495.26, 495.26, 495.26, 495.26]  # 第一组通信开销 (KB)

# 第二组数据 (单位: MB 转换为 KB)
y_values_second = [2.15 * 1024, 3.6 * 1024, 5.0 * 1024, 6.12 * 1024, 7.45 * 1024]  # 第二组通信开销 (KB)

# 创建保存路径
save_path = "E:\\experi\\output\\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 绘制柱状图
plt.figure(figsize=(5, 3))  # 适合论文的尺寸
bar_width = 900  # 控制柱状图宽度

# 绘制第一组数据柱状图
plt.bar([x - bar_width / 2 for x in x_values], y_values_first, width=bar_width, color='lightsalmon', label='SSPQ')
# 绘制第二组数据柱状图
plt.bar([x + bar_width / 2 for x in x_values], y_values_second, width=bar_width, color='lightseagreen', label='[26]')

# 设置标签和坐标轴
plt.xlabel("Number of Data Items", fontsize=12)
plt.ylabel("Communication Cost (KB)", fontsize=12)
plt.xticks(x_values)  # 设置 x 轴刻度
plt.ylim(0, 8000)  # 设置 y 轴的最大值为 8000 KB

# 添加图例和网格线
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图表
output_path = os.path.join(save_path, "comm_search_chart.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 高分辨率保存

print(f"柱状图已保存至: {output_path}")
