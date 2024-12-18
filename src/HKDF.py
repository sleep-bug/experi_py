import hashlib
import hmac
import binascii

from SE import AES256Cipher
from src.config import set_id

salt = b"random_salt_value"
user_id = set_id()

def hkdf_extract(salt: bytes, id_i: bytes, mk: bytes, hash_algo=hashlib.sha256) -> bytes:

    return hmac.new(salt + id_i, mk, hash_algo).digest()


def generate_pwd(prk: bytes, ts: bytes, hash_algo=hashlib.sha256) -> bytes:

    return hmac.new(prk, ts, hash_algo).digest()


def derive_aes_key(prk: bytes, length: int = 32, hash_algo=hashlib.sha256) -> bytes:
    """从 PRK 派生出 AES 密钥，确保是 32 字节。"""
    return hkdf_extract(salt, user_id, prk, hash_algo)[:length]  # 取前 32 字节

