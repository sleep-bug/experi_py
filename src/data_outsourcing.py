import csv
import os
import numpy as np
import pandas as pd

from SHE import Encryption, Decryption
from config import set_pk, set_n, set_f_p, set_pp_sk_H, set_j
from file_operations import write_to_file_as_list
from SPE import compute_z_order, encodeloc
from SSMT import enc, setup


def data_outsourcing():
    # 读取文件
    df = pd.read_csv(r'E:\experi\resource\2000.csv')

    df_x_y = df[['Longitude', 'Latitude']]
    df_x_y.columns = ['x', 'y']
    df_x_y_sorted = df_x_y.sort_values(by='x', ascending=True)


    df_z = df[['Elevation']]
    df_z_sorted = df_z.sort_values(by='Elevation', ascending=True)

    # 保存文件
    df_x_y_sorted.to_csv(r'E:\experi\output\x_y_2000.csv', index=False)
    df_z_sorted.to_csv(r'E:\experi\output\z_2000.csv', index=False)
    print("2000条位置信息已分离.")

    # 处理 x_y.csv 文件
    df_x_y = pd.read_csv(r'E:\experi\output\x_y_2000.csv')
    df_x_y_unique = df_x_y.drop_duplicates(subset=['x', 'y'])
    df_x_y_unique.to_csv(r'E:\experi\output\processed_x_y.csv', index=False)

    # 处理 z.csv 文件
    df_z = pd.read_csv(r'E:\experi\output\z_2000.csv')
    df_z_unique = df_z.drop_duplicates()
    df_z_unique.to_csv(r'E:\experi\output\processed_z.csv', index=False)

    print("文件已处理重复数据")

    with open(r'E:\experi\output\processed_x_y.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        Sp_i = [(int(row[0]), int(row[1])) for row in reader] # Sp_i表示所有(x, y)的坐标
    # (x, y)的处理, 将文件里面的(x, y)都每一个点都进行映射到BF中: BF_Fp_i
    #write_to_file_as_list('Sp_i.txt', Sp_i)
    print(Sp_i)

    Fp_list = []  # 创建一个空列表来保存每个 Fp_i
    z_item_list = [] # 存放所有的z-order交错编码
    for item in range(0, len(Sp_i)):
        z_item = compute_z_order(Sp_i[item][0], Sp_i[item][1])  # (x,y)形成叫做编码
        print(f"第{item}的编码是:", z_item)
        Fp_i = encodeloc(z_item)
        #print(f"第{item}的集合是:", Fp_i)
        z_item_list.append(z_item)
        Fp_list.append(Fp_i)  # 将每个 Fp_i 保存到列表中
    z_max_length_do = max(len(z) for z in z_item_list)
    #print("Z 顺序值的最大位长度", z_max_length_do)
    # 将z_item_list 中的每一项进行加密
    _, sk_H = set_pp_sk_H()
    pk = set_pk()
    H = setup(128)
    E_z_item_list = []
    pp, _ = set_pp_sk_H()
    for idx, element in enumerate(z_item_list):
        # 转换为整数并进行加密
        element = int(element, 2)
        print(element)
        E_z_item = Encryption(element, pk, pp)
        #print(E_z_item)
        E_z_item_list.append(E_z_item)

    E_Fp_i_list = []
    for item in range(0, len(Sp_i)):
        E_Fp_i = enc(pk, H, Fp_list[item])
        E_Fp_i_list.append(E_Fp_i)
        filename = f'E_Fp_i_{item}.txt'
        full_path = os.path.join(r"E:\experi\output\E_Fp_item", filename)
        #write_to_file_as_list(full_path, E_Fp_i)

    # 接下来就是z的处理,
    # 读取 processed_z.csv 文件
    df_z_r = pd.read_csv(r'E:\experi\output\processed_z.csv')
    j = set_j()
    matrix = np.zeros((j, j), dtype=int)
    # 获取 Elevation 列的数据
    elevation_data = df_z_r['Elevation'].tolist()
    # 对每个数值进行映射，确保不超出矩阵范围
    for value in elevation_data:
        # 计算映射位置 (a-1) * j + b
        if  value <= 0 or value > j * j:
            #print(f"警告：数值 {value} 超出矩阵范围")
            continue  # 如果数值超过矩阵范围，跳过

        # 行数从1开始计算，列数也从1开始
        row = (value - 1) // j + 1  # 行数，从1开始
        col = (value - 1) % j + 1  # 列数，从1开始

        # 标记对应位置为1
        matrix[row - 1, col - 1] = 1
    # 打印矩阵
    print("DO外包未加密:\n",matrix)

    # 初始化加密矩阵
    encrypted_matrix_do = np.zeros((j, j), dtype=object)  # 用 dtype=object 支持存储加密对象


    # 对每个元素进行加密
    for i in range(matrix.shape[0]):
        for k in range(matrix.shape[1]):
            m = int(matrix[i, k])  # 将矩阵元素显式转换为整数
            encrypted_matrix_do[i, k] = Encryption(m, pk, pp)  # 加密该值
            #print(f"Encrypted value for element ({i},{j}) = {encrypted_value}")

    # 打印加密后的矩阵（这里只打印密文对象）
    #print(encrypted_matrix_do)

    # 返回值, z_item_list: 所有的点(x, y)形成的z-order码, E_Fp_i_list: Fp_i集合映射的加密的布隆过滤器, z值映射到矩阵(加密)
    return E_z_item_list, E_Fp_i_list, encrypted_matrix_do, z_max_length_do

#data_outsourcing()
