import numpy as np
import matplotlib.pyplot as plt

# 原始数据
x_values = np.array([48, 96, 192, 288])  # 通信开销, 令牌生成阶段
y_values_kb = np.array([727.96, 816.71, 1172.26, 1527.71])  # 单位: KB

# 将通信开销从 KB 转换为 MB
y_values_mb = y_values_kb / 1024

# 插值计算 144 和 240 的通信开销 (MB)
extra_x = np.array([144, 240])
extra_y = np.interp(extra_x, x_values, y_values_mb)

# 合并 x 和 y 值以包括插值点
all_x_values = np.concatenate((x_values, extra_x))
all_y_values = np.concatenate((y_values_mb, extra_y))

# 绘制柱状图
plt.figure(figsize=(5, 3))  # 设置图像大小
bar_width = 24  # 控制柱状宽度（可根据图表调整）

# 使用统一颜色绘制原始数据和插值数据
plt.bar(all_x_values, all_y_values, width=bar_width, color='lightsalmon')

# 添加标签
plt.xlabel('Number of Data Items')
plt.ylabel('Communication Overhead (MB)')
plt.xticks(all_x_values, labels=[str(x) for x in all_x_values])  # 显示所有 x 轴标签

# 创建保存路径
save_path = "E:\\experi\\output\\fig\\comm_token_chart.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')  # 高分辨率保存并去掉边距

print(f"柱状图已保存至: {save_path}")
