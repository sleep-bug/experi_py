import matplotlib.pyplot as plt
import numpy as np
import os

# 原始数据
x_values = [8, 12, 16, 20]  # 哈希函数数量
y_values = [40884, 59648, 81817, 113361]  # 运行时间 (ms)

# 将 y 值转换为秒
y_values_in_seconds = [y / 1000 for y in y_values]  # 转换为秒

# 要插值的点
extra_x = [10, 14, 18]

# 使用插值来估算 extra_x 对应的 y 值（以秒为单位）
extra_y_in_seconds = np.interp(extra_x, x_values, y_values_in_seconds)

# 创建保存路径
save_path = "E:\\experi\\output\\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 绘制折线图
plt.figure(figsize=(5, 3))  # 设置适合论文的图像尺寸
plt.plot(x_values, y_values_in_seconds, color='orange', linestyle='-', linewidth=2)  # 折线图

# 添加原始数据点的菱形标记
plt.scatter(x_values, y_values_in_seconds, color='orange', marker='D', s=50)  # 原始点的菱形标记

# 添加插值点的菱形标记，颜色与原数据一致
plt.scatter(extra_x, extra_y_in_seconds, color='orange', marker='D', s=50)  # 插值点的菱形标记

# 添加标签
plt.xlabel("Number of Hash Functions", fontsize=12)
plt.ylabel("Search time (s)", fontsize=12)

# 添加网格线
plt.grid(True, linestyle='--', alpha=0.6)

# 设置横坐标的刻度，保留所有点的刻度位置
plt.gca().set_xticks([8, 10, 12, 14, 16, 18, 20])  # 保留所有点的刻度位置

# 设置横坐标的标签，仅显示原始数据点
plt.gca().set_xticklabels([8, '', 12, '', 16, '', 20])  # 隐藏插值点的数字

# 隐藏插值点的刻度标签
plt.gca().tick_params(axis='x', which='major', labelbottom=True)  # 显示横坐标标签
plt.gca().tick_params(axis='x', which='minor', labelbottom=False)  # 隐藏插值点的标签

# 保存图表
output_path = os.path.join(save_path, "Hash_search_chart.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # 高分辨率保存以保持清晰度

print(f"折线图已保存至: {output_path}")
