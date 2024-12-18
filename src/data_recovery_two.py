import numpy as np
import pandas as pd
import time
from SE import AES256Cipher
from config import set_j
from data_recovery_one import da_reco1
from file_operations import write_to_file_as_list
from n_schnorr import generate_proof, read_xy_values_from_file, read_values_from_file, verify_proof
from system_initialization import sys_init
from z_order_inverse import z_order_inverse


def da_reco2():
    # 由用户来执行
    _, _, qu_i, _ = sys_init()
    prk_i = qu_i[0]
    SE = AES256Cipher(prk_i)
    r1, r2 = da_reco1()
    C = r1[0]
    l_r = r1[1]
    print("l_r", l_r)
    z_max_length = r1[2]
    print("z_max_length", z_max_length)
    l_z = z_max_length
    # 计算 z_j， j 从 1 到 l_r
    z_list = []  # 用来存储所有 z_j 的值
    for j in range(1, l_r):
        z_j = (C >> (l_z * (j - 1))) % (2 ** l_z)
        z_list.append(z_j)

    # 输出所有 z_j 的值
    print("所有 z_j 的值:", z_list)

    xy_dic = {}
    seen_coordinates = set()  # 用于跟踪已添加的坐标

    for z in z_list:
        coordinate = z_order_inverse(z)
        # 检查坐标是否已存在且不为 (0, 0)
        if coordinate != (0, 0) and coordinate not in seen_coordinates:
            xy_dic[z] = coordinate
            seen_coordinates.add(coordinate)

    # 输出字典
    print("Z-order 编码值与对应坐标的字典:", xy_dic)


    # 对z处理, 减去干扰值, 然后计算位置即所需数值
    # res_dec_matrix是ser2返回的解密的结果矩阵
    # res_enc_matrix_noi 是加密的干扰值矩阵
    res_dec_matrix, res_enc_matrix_noi = r2
    l = set_j()
    # 解密干扰值矩阵
    decrypted_matrix_noi = np.zeros((l, l), dtype=int)  # 存储解密后的矩阵
    for i in range(res_enc_matrix_noi.shape[0]):
        for k in range(res_enc_matrix_noi.shape[1]):
            encrypted_value = res_enc_matrix_noi[i, k]  # 获取加密后的值

            decrypted_bytes = SE.decrypt(encrypted_value)

            decrypted_value = int.from_bytes(decrypted_bytes, byteorder='big')

            decrypted_matrix_noi[i, k] = decrypted_value


    # 打印解密后的矩阵
    #print("解密的干扰值矩阵:")
    #print(decrypted_matrix_noi)
    # 将z矩阵减去干扰值
    matrix = res_dec_matrix - decrypted_matrix_noi
    print("减去干扰值的最终结果矩阵")
    print(matrix)

    # 接下来处理最终的结果
    # 先将所有的(x,y,z)组合起来
    # 初始化一个列表来存储 z 值
    z_list = []

    # 遍历矩阵，找到所有值为 1 的位置
    for a in range(1, l + 1):  # a 是从1开始的行数
        for b in range(1, l + 1):  # b 是从1开始的列数
            if matrix[a - 1, b - 1] == 1:  # 矩阵的索引从0开始，因此这里需要减1
                z = (a - 1) * l + b
                z_list.append(z)

    # 输出计算出的 z 值
    print("计算得到的 z 值：", z_list)

    z_values = z_list

    # 从字典提取 (x, y) 坐标
    xy_values = list(xy_dic.values())
    # 写入文件
    write_to_file_as_list("xy_values.txt", xy_values)
    write_to_file_as_list("z_values.txt", z_values)

    # 生成所有 ((x, y), z) 的组合
    combinations = [((x, y), z) for (x, y) in xy_values for z in z_values]

    # 打印组合的数量
    print(f"总共有 {len(combinations)} 个 ((x, y), z) 组合:")

    # 输出所有组合
    for combo in combinations:
        print(combo)

    return


if __name__ == "__main__":
    # 记录开始时间
    start_time = time.time()
    da_reco2()
    # DO的数据 (x, y, z)
    # 读取CSV文件中的数据
    file_path = 'E:\\experi\\resource\\2000.csv'  # 确保文件路径正确
    data = pd.read_csv(file_path)

    # 用于存储DO生成的数据
    R_i_list = []
    Z_i_list = []
    c_i_list = []
    ts_list = []
    data_x_list = []
    data_y_list = []
    data_z_list = []

    # 提取经度、纬度和海拔高度
    location_data = data[['Longitude', 'Latitude', 'Elevation']].values.tolist()
    for record in location_data:
        data_x = str(record[0])  # 经度
        data_y = str(record[1])  # 纬度
        data_z = str(record[2])  # 高度

        # 时间戳
        ts = "2024-10-15T12:00:00"

        # DO生成签名 (R_i, Z_i, c_i)
        t, Z_i, c_i = generate_proof(data_x, data_y, data_z, ts)

        # 将数据存储到相应的列表中
        R_i_list.append(t)
        Z_i_list.append(Z_i)
        c_i_list.append(c_i)
        ts_list.append(ts)
        data_x_list.append(data_x)
        data_y_list.append(data_y)
        data_z_list.append(data_z)

    # 读取文件数据
    xy_values = read_xy_values_from_file('E:\\experi\\output\\xy_values.txt')  # 假设每行一个 (x, y) 格式
    z_values = read_values_from_file('E:\\experi\\output\\z_values.txt')

    # 用于存储匹配成功的 (x, y, z) 组合
    matched_combinations = set()

    # 遍历每个 (x, y) 坐标
    for xy in xy_values:
        data_x, data_y = xy  # 解包 (x, y)

        # 遍历每个 z 值
        for z in z_values:
            data_z = str(z)

            # 遍历DO的所有数据进行匹配
            for i in range(len(R_i_list)):
                # 提取DO的签名和公钥数据
                ts = ts_list[i]
                R_i = R_i_list[i]
                Z_i = Z_i_list[i]
                c_i = c_i_list[i]

                # 使用QU的数据验证当前组合是否存在于DO的数据中
                result = verify_proof(data_x, data_y, data_z, ts, R_i, Z_i, c_i)

                if result:
                    matched_combinations.add((data_x, data_y, data_z))
                    print(f"匹配成功！组合 (x, y, z): ({data_x}, {data_y}, {data_z}) 在DO的数据中存在")

    # 输出所有匹配成功的组合
    print("\n所有匹配成功的 (x, y, z) 组合：")
    for comb in matched_combinations:
        print((comb[0], comb[1], int(comb[2])))  # 转换为整数输出
    # 记录结束时间并计算总运行时间
    end_time = time.time()
    print(f"数据恢复阶段总运行时间: {end_time - start_time} 秒")
