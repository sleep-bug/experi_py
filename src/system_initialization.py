
import pandas as pd

from MAC import calculate_mac
from SHE import KeyGen, generate_pk
from SSMT import setup
from config import set_k, set_ga_ma, set_n, set_f_p, set_id, set_pp_sk_H, set_j
from HKDF import hkdf_extract
from SE import AES256Cipher
from file_operations import write_to_file_as_list


# 系统初始化，用来返回参数
def sys_init():
    pp, sk_H = set_pp_sk_H()
    pk = generate_pk(pp, sk_H)
    ga_ma = set_ga_ma()
    H = setup(128)

    salt = b"random_salt_value"
    mk = b"master_secret_key"
    user_id = set_id()
    prk_i = hkdf_extract(salt, user_id, mk)

    j = set_j()

    # 计算所有位置信息的MAC_i
    file_path = 'E:\\experi\\resource\\2000.csv'  # 确保文件路径正确
    data = pd.read_csv(file_path)

    location_data = data[['Longitude', 'Latitude', 'Elevation']].values.tolist()

    mac_values = calculate_mac(location_data, prk_i)
    write_to_file_as_list('mac_values.txt', mac_values)

    aes_cipher = AES256Cipher(prk_i)

    ser1 = (prk_i,)
    ser2 = (sk_H,)
    qu = (prk_i, H, j, mac_values)
    pub = (pk, ga_ma)

    return ser1, ser2, qu, pub

#sys_init()