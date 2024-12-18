import ast
import math
import sys
import random
import hashlib
import numpy as np
import sympy as sp
from SHE import KeyGen, Encryption, Decryption, generate_pk
from BF import *
from sympy import symbols
from La_in_modp import lagrange_interpolation, test_lagrange_at_x, lagrange_basis
from SPE import encodearea
from file_operations import *
from bootstrapping import *
from config import set_pk, set_pp_sk_H, x_values, y_values, p, set_n, set_f_p, set_S
from hash_fun import generate_hash_functions

pp, sk_H = set_pp_sk_H()
ga_ma = set_ga_ma()
m = set_m()


def setup(λ):

    global m

    ga_ma = set_ga_ma()

    hash_funcs = generate_hash_functions(ga_ma)
    return hash_funcs


def interpolation(ga_ma, p):
    """
    调用lagrange_interpolation方法，生成并输出插值多项式
    """

    fx = test_lagrange_at_x  # 系数低到高
    for i in range(ga_ma + 1):
        print(f"fx({i}) = {fx(i)}")

    return fx


def enc(pk, H, S):
    """
    将 set S 中的每一个元素都映射到 BF 中，并加密
    """
    global m

    hash_funcs = setup(128)
    bf = BloomFilter(hash_funcs, m)

    for item in S:
        bf.add(item)

    encrypted_bitarray = bf.encrypt_bitarray(pk)  # Assuming encrypt_bitarray is correctly defined in BF

    return encrypted_bitarray

def tokengen(pk, H, e):
    """
    将元素 e 中的每一个元素都映射到 BF 中，并加密
    """
    # 初始一个 Bloom Filter
    global m, pp
    ga_ma = set_ga_ma()
    hash_funcs = setup(128)
    bf = BloomFilter(hash_funcs, m)

    bf.add(e)

    #print("e未加密的 bit_array:", bf.bit_array)
    write_to_file_as_list("BF_e.txt", bf.bit_array)

    encrypted_bitarray = bf.encrypt_bitarray(pk)  # Assuming encrypt_bitarray is correctly defined in BF

    write_to_file_as_list("E_BF_e.txt", encrypted_bitarray)

    return encrypted_bitarray

def check(E_BF_S, E_BF_e, fx): #fx函数, 模p 暂时不要
    """
    返回 E_result = E_0 或者 E_1
    """
    if len(E_BF_S) != len(E_BF_e):
        raise ValueError("E_BF_S and E_BF_e must have the same length")

    multiplied_bits = [E_BF_S[i] * E_BF_e[i] for i in range(len(E_BF_S))]
    write_to_file_as_list("multiplied_bits.txt", multiplied_bits)

    sys.set_int_max_str_digits(100000)

    E_sig_ma = sum(int(bit) for bit in multiplied_bits)

    ret_sig_ma = Decryption(sk_H, E_sig_ma)


    ga_ma = set_ga_ma()

    if ret_sig_ma == ga_ma:
        E_result = Encryption(1, pk, pp)
    else:
        E_result = Encryption(0, pk, pp)


    return E_result

def decrypt_bloom_filter(sk_H, encrypted_bitarray):
    """
    解密布隆过滤器中的每一位，并输出解密后的布隆过滤器
    :param sk_H: 解密密钥
    :param encrypted_bitarray: 已加密的布隆过滤器位数组
    :param L: 参数L，解密需要
    :return: 解密后的位数组
    """
    decrypted_bitarray = []

    for ciphertext in encrypted_bitarray:
        decrypted_bit = Decryption(sk_H, ciphertext)
        decrypted_bitarray.append(decrypted_bit)

    print("解密后的 bit_array:", decrypted_bitarray)

    return decrypted_bitarray

