import random
import sympy


# 生成素数函数
def generate_prime(bits):
    """生成一个指定位数的素数"""
    return sympy.randprime(2 ** (bits - 1), 2 ** bits)

# KeyGen方法
def KeyGen(k0, k1, k2, k3):
    """生成公共参数和秘钥"""
    g1 = generate_prime(k0)
    L = random.getrandbits(k2)
    num_primes = (k3 + k0 - 1) // k0
    g2_primes = [generate_prime(k0) for _ in range(num_primes)]
    g2 = 1
    for prime in g2_primes:
        g2 *= prime
    N = g1 * g2

    pp = (k0, k1, k2, k3, N)
    sk_H = (g1, L)
    return pp, sk_H

def generate_pk(pp, sk_H):
    """生成并返回 pk"""
    k0, k1, k2, k3, N = pp
    E_0 = encrypt_value(0, sk_H, k2, k3, N)
    E_neg1 = encrypt_value(-1, sk_H, k2, k3, N)
    E_1 = encrypt_value(1, sk_H, k2, k3, N)

    pk = (E_0, E_neg1, E_1)  # 返回 pk，而不是修改全局变量
    return pk

# Encryption方法 with pk = {E(0), E(-1), E(1)}
def Encryption(m, pk, pp):
    """加密消息 m 使用公共参数 pk"""

    k0, k1, k2, k3, N = pp

    E_0, E_neg1, E_1 = pk

    r_dot = random.getrandbits(k2)
    r_ddot = random.getrandbits(k2)

    term1 = m + r_dot * (E_neg1 + E_1)
    term2 = r_ddot * E_0
    ciphertext = (term1 + term2) % N
    return ciphertext

# 加密函数E(x) for specific values
def encrypt_value(x, sk_H, k2, k3, N):
    """Encrypt specific values like E(0), E(1), E(-1)"""
    g1, L = sk_H
    r1 = ''.join(random.choice('01') for _ in range(k2))
    r2 = ''.join(random.choice('01') for _ in range(k3))

    r1_inte = int(r1, 2)
    r2_inte = int(r2, 2)

    term1 = (r1_inte * L + x)
    term2 = 1 + r2_inte * g1
    ciphertext = (term1 * term2) % N
    return ciphertext

# Decryption方法
def Decryption(sk_H, ciphertext):
    g1, L = sk_H
    m_prime = ciphertext % g1
    m_prime = m_prime % L
    if m_prime < L // 2:
        m = m_prime
    else:
        m = m_prime - L
    return m


# 加法性质-I：E(m1) + E(m2) mod N -> E(m1 + m2)
def additive_property_I(ciphertext1, ciphertext2, N):
    return (ciphertext1 + ciphertext2) % N

# 加法性质-II：E(m1) + m2 mod N -> E(m1 + m2)
def additive_property_II(ciphertext1, m2, N):
    return (ciphertext1 + m2) % N

# 乘法性质-I：E(m1) * E(m2) mod N -> E(m1 * m2)
def multiplicative_property_I(ciphertext1, ciphertext2, N):
    result = (ciphertext1 * ciphertext2) % N
    return result

# 乘法性质-II：E(m1) * m2 mod N -> E(m1 * m2)
def multiplicative_property_II(ciphertext1, m2, N):
    return (ciphertext1 * m2) % N



