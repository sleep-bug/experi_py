import json
import numpy as np
import pandas as pd
from numpy.matrixlib.defmatrix import matrix

from SSMT import check, interpolation, decrypt_bloom_filter
from bootstrapping import Bootstrapping
from config import set_ga_ma, p, set_m, set_j
from data_outsourcing import data_outsourcing
from remove_perturbations import remove_perturbations
from system_initialization import sys_init
from token_generatioin_two import tok_gene_two
from SE import AES256Cipher
# 进行搜索工作

def search():
    ser1, _, _, _ = sys_init()
    # 获取外包数据, 包括 所有的z-order编码列表, 所有的每个(x,y)对应的Fp的BF列表
    E_z_item_list, E_Fp_i_list, encrypted_matrix_do, z_max_length_do = data_outsourcing()

    # 获得令牌数据, 加密的干扰的BF ， 加密的干扰值
    token_1, token_2 = tok_gene_two()
    e_bf_S_A_pri_list, e_S_pert_list, z_max_length_to = token_1 # 加密的BF(已经添加干扰值), 加密的干扰值
    encrypted_matrix_to, enc_matrix_noi = token_2 # 加密的z矩阵, 加密的干扰值矩阵
    # Z 顺序值的最大位长度, 应该是 来自DO的z-order的最大长度
    z_max_length = z_max_length_do

    # 解密干扰值，
    prk_i = ser1[0]
    SE = AES256Cipher(prk_i)
    pertur_list = []
    for idx, element in enumerate(e_S_pert_list):
        # 解密干扰值
        decrypted_pert = SE.decrypt(element)
        # 假设解密后是字符串，将其转换为整数列表
        pertur_list.append([int(bit) for bit in decrypted_pert.decode('utf-8')])

    # 去除干扰值
    e_bf_S_A_list = []
    for idx, element in enumerate(e_bf_S_A_pri_list):
        e_bf_S_A = remove_perturbations(element, pertur_list[idx])
        e_bf_S_A_list.append(e_bf_S_A)


    # 使用for循环来检测所有的e_bf_S_A_list中的与E_Fp_i_list中的一项一项的检测
    # 使用check() 来判断是否Fp属于S_A
    #check(e_S_pert, E_Fp_i_list[0], )
    _, ser2, _, _ = sys_init()

    # 获取插值函数
    ga_ma = set_ga_ma()
    global p
    fx = interpolation(ga_ma, p)  # 系数低到高
    e_res_list = []
    for idx1, element in enumerate(E_Fp_i_list):
        e_res = 0
        for idx2, ele in enumerate(e_bf_S_A_list):
            guo = check(element, ele, fx) # 返回加密的1 或 0
            e_res  = e_res  + guo

        e_res_list.append(e_res)

    e_al_list = []
    for i in range(len(e_res_list)):
        e_al = e_res_list[i] * E_z_item_list[i]
        e_al_list.append(e_al)
    #print('e_res_list', e_res_list)


    # 将多有结果集合成一个结果, 保护访问模式
    l_z = z_max_length
    l_r = len(e_res_list)
    E_C = 0

    for idx, element in enumerate(e_al_list):
        ele = Bootstrapping(element)
        e_C = ele * 2 ** (idx * l_z)
        E_C += e_C

    # 接下来处理 z矩阵相乘.
    # 利用Hadamard乘积
    # 解密干扰值矩阵
    j = set_j()
    decrypted_matrix_noi = np.zeros((j, j), dtype=int)  # 存储解密后的矩阵
    for i in range(enc_matrix_noi.shape[0]):
        for k in range(enc_matrix_noi.shape[1]):
            encrypted_value = enc_matrix_noi[i, k]  # 获取加密后的值

            decrypted_bytes = SE.decrypt(encrypted_value)

            decrypted_value = int.from_bytes(decrypted_bytes, byteorder='big')

            decrypted_matrix_noi[i, k] = decrypted_value


    # 打印解密后的干扰值矩阵
    #print("ser2解密的干扰值矩阵:")
    #print(decrypted_matrix_noi)

    # 将z矩阵减去干扰值
    matri = encrypted_matrix_to - decrypted_matrix_noi

    # hadamard乘积
    res_mat = matri * encrypted_matrix_do

    # 对结果矩阵添加干扰值
    # 生成一个j x j的矩阵，干扰值为1到9之间的随机整数
    res_noise_matrix = np.random.randint(1, 10, size=(j, j))
    # 将干扰矩阵加密, 先初始化加密矩阵
    res_enc_matrix_noi = np.zeros((j, j), dtype=object)  # 用 dtype=object 支持存储加密对象

    # 对每个元素进行加密
    for i in range(res_noise_matrix.shape[0]):
        for k in range(res_noise_matrix.shape[1]):
            m = int(res_noise_matrix[i, k])  # 将矩阵元素显式转换为整数

            # 将整数转换为 4 字节（根据数据范围）进行加密
            m_bytes = m.to_bytes(4, byteorder='big')  # 4字节，‘big’表示大端字节序
            res_enc_matrix_noi[i, k] = SE.encrypt(m_bytes)  # 加密该值
    # 打印加密后的矩阵（这里只打印密文对象）
    #print("ser结果加密\n", res_enc_matrix_noi)

    # 将结果矩阵和干扰值矩阵加密
    res_matrix = res_mat + res_noise_matrix

    res1 = (E_C, l_r, z_max_length)
    res2 = (res_matrix, res_enc_matrix_noi)

    return res1, res2

#search()