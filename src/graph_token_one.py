import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# \gamma的变化对令牌生成的影响


# 原始数据集1
x_values = [8, 12, 16, 20]
y_values = [260, 275.3, 283, 300]  # 单位为毫秒 (ms)
y_values = [y / 1000 for y in y_values]  # 转换为秒

# 第二组数据集2的y值
y_values_2 = [7035, 7089, 7150, 7384]  # 单位为毫秒
y_values_2 = [y / 1000 for y in y_values_2]  # 转换为秒

# 插值点
extra_x = [10, 14, 18]
extra_y = np.interp(extra_x, x_values, y_values)       # 第一组插值结果
extra_y_2 = np.interp(extra_x, x_values, y_values_2)  # 第二组插值结果

# 创建保存路径
save_path = "E:\\experi\\output\\fig"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 创建图表和主轴
fig, ax = plt.subplots(figsize=(5, 3))

# 绘制第一组数据
ax.plot(x_values, y_values, color='#FFA07A', linestyle='-', linewidth=2, marker='o', markersize=5, label="Token generation Ⅰ")
ax.scatter(x_values + extra_x, y_values + list(extra_y), color='#FFA07A', marker='o', s=30)  # 使用小圆点

# 绘制第二组数据
ax.plot(x_values, y_values_2, color='#FFDAB9', linestyle='-', linewidth=2, marker='o', markersize=5, label="Token generation Ⅱ")
ax.scatter(x_values + extra_x, y_values_2 + list(extra_y_2), color='#FFDAB9', marker='o', s=30)  # 使用小圆点

# 设置横坐标刻度
ax.set_xticks(x_values + extra_x)

# 设置主轴标签
ax.set_xlabel("Number of data Items", fontsize=12)
ax.set_ylabel("Token generation time (s)", fontsize=12)

# 设置 y 轴的范围为 (0, 10)
ax.set_ylim(0, 10)

# 添加图例在左上角
ax.legend(loc="upper left")

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.6)

# 设置横坐标的刻度，保留所有点的刻度位置
plt.gca().set_xticks([8, 10, 12, 14, 16, 18, 20])  # 保留所有点的刻度位置

# 设置横坐标的标签，仅显示原始数据点
plt.gca().set_xticklabels([8, '', 12, '', 16, '', 20])  # 隐藏插值点的数字

# 隐藏插值点的刻度标签
plt.gca().tick_params(axis='x', which='major', labelbottom=True)  # 显示横坐标标签
plt.gca().tick_params(axis='x', which='minor', labelbottom=False)  # 隐藏插值点的标签

# 创建放大视图
ax_inset = inset_axes(ax, width=1.5, height=1.0, loc="center right", bbox_to_anchor=(0.99, 0.35), bbox_transform=ax.transAxes)

# 在放大视图中绘制第一组数据的细节
ax_inset.plot(x_values, y_values, color='#FFA07A', linestyle='-', linewidth=2, marker='o', markersize=5)
ax_inset.scatter(extra_x, extra_y, color='#FFA07A', marker='o', s=30)

# 设置放大视图的坐标范围，聚焦于有明显差异的部分
ax_inset.set_xlim(8, 20)
ax_inset.set_ylim(min(y_values) - 0.01, max(y_values) + 0.01)

# 隐藏放大视图的刻度标签
ax_inset.set_xticks([])
ax_inset.set_yticks([])

# 保存图表
output_path = os.path.join(save_path, "Token_with_inset.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"折线图已保存至: {output_path}")
