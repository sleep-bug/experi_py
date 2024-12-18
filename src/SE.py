# 使用AES-256 来进行

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

class AES256Cipher:
    def __init__(self, key: bytes):
        """
        初始化 AES-256 加密器。
        :param key: 必须是 32 字节的 AES 密钥。
        """
        assert len(key) == 32, "AES-256 密钥长度必须是 32 字节（256 位）"
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        """
        加密数据。
        :param data: 需要加密的明文数据，字节类型。
        :return: 加密后的数据，包含 IV 和密文。
        """
        iv = os.urandom(16)  # 生成随机的 IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))  # 明文填充后加密
        return iv + ciphertext  # 返回包含 IV 的密文

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        解密数据。
        :param encrypted_data: 需要解密的数据，包含 IV 和密文。
        :return: 解密后的明文数据，字节类型。
        """
        iv = encrypted_data[:16]  # 提取 IV
        ciphertext = encrypted_data[16:]  # 提取密文
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)  # 解密并去除填充
