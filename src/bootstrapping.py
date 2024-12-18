
from SHE import Encryption, Decryption
from config import set_pk, set_pp_sk_H, set_m, set_ga_ma

import random

pp, sk_H= set_pp_sk_H()
pk = set_pk()

# Bootstrapping Protocol
def Bootstrapping(ciphertext):
    """
    对密文执行引导操作，刷新为新密文。

    参数:
    - ciphertext: 需要刷新的密文
    - pk: 公钥，包含 {E(0), E(-1), E(1)}
    - sk_H: 私钥，包含 (g1, L)
    - pp: 公共参数，包含 {k0, k1, k2, k3, N}

    返回:
    - 新的加密密文
    """

    # Step 1: S1 选择一个随机数 r1
    r1 = random.getrandbits(pp[2])  # 生成随机数 r1 (pp[2] 是 k2)
    if random.choice([True, False]):
        r1 = -r1  # 随机选择 r1 为负数或正数

    # Step 2: S1 计算 E(m + r1)
    if r1 < 0:
        E_m_r1 = (ciphertext + abs(r1) * pk[1]) % pp[4]  # pk[1] 是 E(-1)
    else:
        E_m_r1 = (ciphertext + r1 * pk[2]) % pp[4]  # pk[2] 是 E(1)

    # Step 3: S2 解密 E(m + r1) 并返回重新加密的 E(m')
    m_prime = Decryption(sk_H, E_m_r1)
    E_m_prime = Encryption(m_prime, pk, pp)

    # Step 4: S1 根据 r1 生成新的密文 E(m)
    if r1 < 0:
        new_ciphertext = (E_m_prime + abs(r1) * pk[2]) % pp[4]  # pk[2] 是 E(1)
    else:
        new_ciphertext = (E_m_prime + r1 * pk[1]) % pp[4]  # pk[1] 是 E(-1)

    return new_ciphertext


