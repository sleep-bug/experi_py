import hashlib
import random
import pandas as pd

# 设置大素数p和生成元g
ppp = 2 ** 256 - 189  # 选取一个大素数p（示例用的256位素数）
g = 2  # 生成元g

# 哈希函数，用于生成x_i和挑战c_i
def hash_func(data):
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)

def generate_proof(x, y, z, ts):
    xy_hash = hash_func(f"{x},{y}")
    z_hash = hash_func(f"{z}")
    x_i = xy_hash ^ z_hash

    y_i = pow(g, x_i, ppp)

    # 生成随机数r_i
    r_i = random.randint(1, ppp - 1)

    t = pow(g, r_i, ppp)

    c_i = hash_func(f"{y_i},{t},{ts}")

    Z_i = (r_i + c_i * x_i) % (ppp - 1)

    return t, Z_i, c_i


def verify_proof(x, y, z, ts, t, Z_i, c_i):
    xy_hash = hash_func(f"{x},{y}")
    z_hash = hash_func(f"{z}")
    x_i_prime = xy_hash ^ z_hash

    y_i_prime = pow(g, x_i_prime, ppp)

    lhs = pow(g, Z_i, ppp)  # g^Z_i mod p
    rhs = (t * pow(y_i_prime, c_i, ppp)) % ppp  # t * (y_i')^c_i mod p

    return lhs == rhs

# 从文件读取 z_values 数据
def read_values_from_file(file_path):
    with open(file_path, 'r') as file:
        cleaned_data = file.read().strip().replace('[', '').replace(']', '').replace(' ', '')

        values = [int(value) for value in cleaned_data.split(',')]
    return values

# 从文件读取 xy_values 数据
def read_xy_values_from_file(file_path):
    with open(file_path, 'r') as file:
        # 读取并清理文件内容
        cleaned_data = file.read().strip().replace('[', '').replace(']', '').replace(' ', '')
        # 分割并解析为元组
        pairs = cleaned_data.split('),(')
        xy_values = [tuple(map(int, pair.strip('()').split(','))) for pair in pairs]
        return xy_values
