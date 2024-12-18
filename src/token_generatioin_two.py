import json
import os
import numpy as np
import pandas as pd
from SHE import encrypt_value, Decryption
from config import set_k, set_N, set_pp_sk_H, set_j
from file_operations import write_to_file_as_list
from remove_perturbations import remove_perturbations
from token_generatioin_one import tok_gene_one
from system_initialization import sys_init
from BF import BloomFilter

def tok_gene_two():
    # 令牌 com_matrix是带有干扰值的 z矩阵; enc_matrix_noi是加密的干扰值矩阵
    # e_S_pert_list是加密的干扰值列表; bf_S_A_pri_list是加了干扰值未加密的BF
    # z_max_length是z-order的最大长度, 来自DO的z-order
    e_S_pert_list, bf_S_A_pri_list, z_max_length_to, com_matrix, enc_matrix_noi = tok_gene_one()
    _, ser2, _, _ = sys_init()
    sk_H = ser2[0]
    pp, _ = set_pp_sk_H()

    k0, k1, k2, k3 = set_k()
    N = set_N()
    #print({f"添加干扰值的BF:{bf_S_A_pri}"})

    e_bf_S_A_pri_list = []
    for idx, element in enumerate(bf_S_A_pri_list):
        e_bf_S_A_pri = []
        for item in element:
            # 服务器2 拥有私钥, 可以利用私钥进行加密
            e_bf_S_A_pri.append(encrypt_value(item, sk_H, k2, k3, N))
        e_bf_S_A_pri_list.append(e_bf_S_A_pri)
        filename = f'e_bf_S_A_pri_{idx}.txt'
        full_path = os.path.join(r"E:\experi\output\e_bf_S_A_pri", filename)
        write_to_file_as_list(full_path, e_bf_S_A_pri)


    # 接下来处理z-order矩阵
    # 对来自qu的z矩阵进行加密
    # 初始化加密矩阵
    j = set_j()
    encrypted_matrix_to = np.zeros((j, j), dtype=object)  # 用 dtype=object 支持存储加密对象

    # 对每个元素进行加密
    for i in range(com_matrix.shape[0]):
        for k in range(com_matrix.shape[1]):
            m = int(com_matrix[i, k])  # 将矩阵元素显式转换为整数
            encrypted_matrix_to[i, k] = encrypt_value(m, sk_H, k2, k3, N)   # 加密该值
            # print(f"Encrypted value for element ({i},{j}) = {encrypted_value}")

    # 打印加密后的矩阵（这里只打印密文对象）
    #print(encrypted_matrix_to)

    token_1 = (e_bf_S_A_pri_list, e_S_pert_list, z_max_length_to) # 加密的BF(已经添加干扰值), 加密的干扰值

    token_2 = (encrypted_matrix_to, enc_matrix_noi) # 加密的z矩阵, 加密的干扰值矩阵

    return token_1, token_2

#tok_gene_two()