import numpy as np
from potime import RunTime

from SHE import Decryption
from config import set_j
from search import search
from system_initialization import sys_init
import sys
import numpy as np


def da_reco1():
    # 获取搜索结果
    res1, res2 = search()
    # 对(x,y)进行处理 -- 由ser2 来进行解密
    E_C = res1[0]
    l_r = res1[1]
    z_max_length = res1[2]
    _, ser2, _, _ = sys_init()
    sk_H = ser2[0]
    # 解密
    C = Decryption(sk_H, E_C)
    r1 = (C, l_r, z_max_length)

    # 对z进行处理 -- 由ser2 来进行解密
    res_matrix, res_enc_matrix_noi = res2
    j = set_j()
    # 初始化解密后的矩阵
    res_dec_matrix = np.zeros((j, j), dtype=int)

    # 对每个元素进行解密
    for i in range(j):
        for k in range(j):
            ciphertext = res_matrix[i, k]
            decrypted_value = Decryption(sk_H, ciphertext)  # 对每个元素进行解密
            res_dec_matrix[i, k] = decrypted_value  # 将解密后的值存入解密矩阵中

    # 打印解密后的矩阵
    print("解密后的矩阵", res_dec_matrix)
    r2 = (res_dec_matrix, res_enc_matrix_noi)


    return r1, r2

#da_reco1()

