import math
import time
import struct
import numpy as np
import csv

from SHE import KeyGen, generate_pk

# 文件路径
#file_path = r'E:\experi\output\elevation_list.txt'

def set_S():
    with open(r'E:\experi\resource\xy_coordinates_unique.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        S = [(int(row[0]), int(row[1])) for row in reader]
    return S

_cached_pp = None
_cached_sk_H = None

def set_pp_sk_H():
    global _cached_pp, _cached_sk_H
    if _cached_pp is None:
        k0, k1, k2, k3 = set_k()  # Example bit lengths
        _cached_pp, _cached_sk_H = KeyGen(k0, k1, k2, k3)
    return _cached_pp, _cached_sk_H


def set_N():
    pp, _ = set_pp_sk_H()
    N = pp[4]
    return N

def set_pk():
    pp, sk_H = set_pp_sk_H()
    pk = generate_pk(pp, sk_H)
    return pk

def set_n():
    n = 8
    return n

def set_f_p():
    f_p = 0.0001 # 误报率
    return f_p

# BF_size
def set_m():
    n = set_n()
    f_p = set_f_p()
    return int(- (n * math.log(f_p)) / (math.log(2) ** 2))

def set_ga_ma():
    m = set_m()
    n = set_n()
    return math.floor((m / n) * math.log(2))

def set_id():
    id_i = "user123"  # 用户的身份 ID
    id_i_bytes = id_i.encode('utf-8')
    return id_i_bytes    # 用户身份 (byte string)

def set_ts():
    timestamp_millis = int(time.time() * 1000)

    # 将时间戳转换为字节字符串
    ts = struct.pack('>Q', timestamp_millis)  # 使用大端字节序打包为字节字符串
    return ts

def set_k():
    k0, k1, k2, k3 = 2024, 30, 80, 2024

    return k0, k1, k2, k3

_cached_j = None
def set_j():
    global _cached_j
    _cached_j = 20
    return _cached_j



p = N = set_N()  # 生成一个4048位的大素数

# 生成 x 和 y 数据集
x_values = np.arange(set_ga_ma() + 1)
y_values = np.zeros(set_ga_ma() + 1, dtype=int)
y_values[-1] = 1  # 最后一个点的 y 值为 1
