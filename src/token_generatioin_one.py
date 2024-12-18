import csv
import json
import os

import bitarray
import numpy as np
import pandas as pd

from SHE import Encryption
from SPE import encodearea
from config import set_S, set_pk, set_n, set_f_p, set_m, set_j
from file_operations import write_to_file_as_list
from SSMT import enc, setup, decrypt_bloom_filter
from BF import BloomFilter
from remove_perturbations import remove_perturbations
from system_initialization import sys_init
from SE import AES256Cipher


from potime import RunTime

# 查询用户进行对数据的处理和利用辅助服务器令牌生成
@RunTime
def tok_gene_one():
    # 获取数据
    A = set_S()
    #write_to_file_as_list('x_y.txt', A)

    #进行z-order编码 z_orders_a
    z_orders_a, valid_prefixes, no_valid_prefixes = encodearea(A)
    S_A = set(valid_prefixes + no_valid_prefixes)

    print("最终集合S：", S_A)
    z_max_length_to = max(len(z) for z in z_orders_a)
    print("Z 顺序值的最大位长度", z_max_length_to)

    # 将集合映射到一个BF中, 先求集合长度n
    S_A_len = len(S_A)
    print(f"S_A的长度是{S_A_len}")

    m = set_m()
    hash_funcs = setup(128)

    bf_S_A_list = []
    # 将 集合 S_A 的元素 分别映射 一个元素对应一个BF
    for idx, element in enumerate(S_A):
        # 每一个元素对应一个BF
        bf_idx = BloomFilter(hash_funcs, m)
        bf_idx.add(element)
        bf_S_A_list.append(bf_idx)
        filename = f'bf_S_A_{idx}.txt'
        full_path = os.path.join(r"E:\experi\output\bf_S_A", filename)
        #write_to_file_as_list(full_path, bf_idx.bit_array)

    e_S_pert_list = []
    bf_S_A_pri_list = []
    _, _, qu_i, _ = sys_init()
    prk_i = qu_i[0]
    SE = AES256Cipher(prk_i)
    # 添加干扰值
    for idx, element in enumerate(bf_S_A_list):
        filename = f'perturbations{idx}.txt'
        bf_S_A_pri, S_pert = element.add_perturbations(filename)
        bf_S_A_pri_list.append(bf_S_A_pri)
        # 将干扰值进行加密
        # e_S_pert 加密的干扰值
        S_pert_str = ''.join(str(bit) for bit in S_pert)  # 将列表中的每个元素转换为字符串并连接
        e_S_pert = SE.encrypt(S_pert_str.encode('utf-8'))  # 使用连接后的字符串进行加密
        e_S_pert_list.append(e_S_pert)

    # 读取 processed_z.csv 文件
    df_z_r = pd.read_csv(r'E:\experi\output\z_coordinates_unique.csv')
    j = set_j()
    matrix = np.zeros((j, j), dtype=int)

    elevation_data = df_z_r['Elevation'].tolist()

    for value in elevation_data:
        # 计算映射位置 (a-1) * j + b
        if value <= 0 or value > j * j:
            #print(f"警告：数值 {value} 超出矩阵范围")
            continue  # 如果数值超过矩阵范围，跳过

        # 行数从1开始计算，列数也从1开始
        row = (value - 1) // j + 1  # 行数，从1开始
        col = (value - 1) % j + 1  # 列数，从1开始

        # 标记对应位置为1
        matrix[row - 1, col - 1] = 1
    # 打印矩阵
    print("qu请求未加密\n", matrix)

    noise_matrix = np.random.randint(1, 10, size=(j, j))

    # 将干扰矩阵加密, 先初始化加密矩阵
    enc_matrix_noi = np.zeros((j, j), dtype=object)  # 用 dtype=object 支持存储加密对象

    # 对每个元素进行加密
    for i in range(noise_matrix.shape[0]):
        for k in range(noise_matrix.shape[1]):
            m = int(noise_matrix[i, k])  # 将矩阵元素显式转换为整数

            # 将整数转换为 4 字节（根据数据范围）进行加密
            m_bytes = m.to_bytes(4, byteorder='big')  # 4字节，‘big’表示大端字节序
            enc_matrix_noi[i, k] = SE.encrypt(m_bytes)  # 加密该值

    # 例如，将映射矩阵和干扰矩阵相加
    com_matrix = matrix + noise_matrix
    #print("添加干扰值的矩阵:\n", com_matrix)

    # 返回值, 令牌生成第一阶段, 发送给Ser2, 加密的干扰值列表, 未加密但加干扰值的z-order映射的BF, z-order最大位长度, 加了干扰值的矩阵, 还有干扰值矩阵
    return e_S_pert_list, bf_S_A_pri_list, z_max_length_to, com_matrix, enc_matrix_noi


#tok_gene_one()
