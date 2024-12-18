import matplotlib.pyplot as plt
import numpy as np

# 定义体素空间
x, y, z = np.indices((10, 10, 10))  # 对应坐标范围 0-9

# 定义三个 1x1x1 的立方体的位置
cube1 = (x == 4) & (y == 4) & (z == 7)  # 体素 1：坐标 (4, 4, 7)
cube2 = (x == 5) & (y == 4) & (z == 7)  # 体素 2：坐标 (5, 4, 7)
cube3 = (x == 4) & (y == 5) & (z == 7)  # 体素 3：坐标 (4, 5, 7)

# 合并所有体素
voxels = cube1 | cube2 | cube3

# 定义颜色（半透明白色）
colors = np.zeros(voxels.shape + (4,), dtype=float)  # 初始化 RGBA
colors[voxels] = [1, 1, 1, 0.6]  # 白色，透明度 0.6（调整透明度）

# 绘制体素
fig = plt.figure(figsize=(22, 14))  # 更大图像宽度和高度
ax = fig.add_subplot(111, projection='3d')
ax.voxels(voxels, facecolors=colors, edgecolor='k')  # 显示体素

# 设置坐标轴范围（确保起点为零）
ax.set_xlim(0, 10)  # x 轴范围
ax.set_ylim(0, 10)  # y 轴范围
ax.set_zlim(0, 10)  # z 轴范围

# 设置 x、y 和 z 轴刻度为 1 间隔，去掉 10
ax.set_xticks(np.arange(0, 10, 1))  # x 轴刻度（不包括10）
ax.set_yticks(np.arange(0, 10, 1))  # y 轴刻度（不包括10）
ax.set_zticks(np.arange(0, 10, 1))  # z 轴刻度（不包括10）

# 调整坐标轴刻度字体大小
ax.tick_params(axis='both', which='major', labelsize=20)  # x 和 y 轴的刻度
ax.tick_params(axis='z', which='major', labelsize=20)  # z 轴的刻度

# 在 Y=0 平面上绘制圆点 (5, 0, 8) 和 (5, 0, 7)
ax.scatter(5, 0, 8, color='blue', s=40)  # 使用蓝色，调整圆点大小
ax.scatter(5, 0, 7, color='blue', s=40)  # 使用蓝色，调整圆点大小

# 绘制投影的虚线，投影到 x-y 平面
# 找到所有体素的顶点
for i, j, k in zip(*np.where(voxels)):  # 找到所有体素位置
    # 顶点的坐标 (体素的 4 个角)
    x_coords = [i, i+1, i+1, i]
    y_coords = [j, j, j+1, j+1]
    z_coord = k  # z 为当前体素的高度

    # 投影到 x-y 平面（z=0），并绘制虚线
    for x0, y0 in zip(x_coords, y_coords):
        ax.plot([x0, x0], [y0, y0], [0, z_coord], color='gray', linestyle='--', linewidth=1)

# 绘制投影区域的边界
boundary_x = [4, 6, 6, 5, 5, 4, 4]  # 包含起点和终点
boundary_y = [4, 4, 5, 5, 6, 6, 4]  # 包含起点和终点
boundary_z = [0, 0, 0, 0, 0, 0, 0]  # z 坐标固定为 0（x-y 平面）

ax.plot(boundary_x, boundary_y, boundary_z, color=(0.5, 0.7, 1), linestyle='-', linewidth=2)

# **填充给定区域**
# 使用填充函数 fill_betweenx 来填充区域
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 定义填充区域的 4 个点（x, y, z）
vertices = [
    [(4, 4, 0), (6, 4, 0), (6, 5, 0), (5, 5, 0), (5, 6, 0), (4, 6, 0)]
]

# 创建一个 Poly3DCollection 对象
poly3d = Poly3DCollection(vertices, color='lightgray', alpha=0.5)
ax.add_collection3d(poly3d)  # 将该区域添加到 3D 图中

# 设置标签
ax.set_xlabel('X-axis', fontsize=25, labelpad=20)  # 调整 X 轴标签的字体大小和与轴的距离
ax.set_ylabel('Y-axis', fontsize=25, labelpad=20)  # 调整 Y 轴标签的字体大小和与轴的距离
ax.set_zlabel('Z-axis', fontsize=25, labelpad=5)  # 调整 Z 轴标签的字体大小和与轴的距离

# 标注 (4,4,8) 和 (6,4,8) 位置，并确保文本稍微在点的上方
# 使用 Times New Roman 字体，增加字体大小并调整位置
ax.text(4, 4, 8 + 0.2, '(4,4,8)', color='red', fontsize=30, weight='bold', fontname='Times New Roman')
ax.text(7.8, 4, 8.5, '(6,4,8)', color='red', fontsize=30, weight='bold', fontname='Times New Roman')
ax.scatter(4, 4, 8, color='red', s=40)  # (4, 4, 8)
ax.scatter(6, 4, 8, color='red', s=40)  # (6, 4, 8)

# 在合适的位置添加 Z = {7, 8} 的文本
ax.text(9.5, 2, 9.2, 'Z = {7, 8}', color='blue', fontsize=30, fontname='Times New Roman', weight='bold', rotation=180)
# 调整视角
ax.view_init(30, 45)

# 手动调整边距，确保图形显示完整
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)  # 调整边距

# 保存图像
plt.tight_layout(pad=2.0)  # 自动调整布局，避免图形元素重叠
plt.savefig('3D_projection.png', dpi=300, bbox_inches='tight', pad_inches=0.1)  # 保存为高分辨率图像

# 显示图形
plt.show()
