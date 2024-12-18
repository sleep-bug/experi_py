import hmac
import hashlib
from HKDF import hkdf_extract
from config import set_id

# 计算 MAC 值的函数
def calculate_mac(location_data, secret_key):
    macs = []
    for (x, y, z) in location_data:
        # 将位置信息转换为字符串
        message = f"{x},{y},{z}".encode()
        # 计算 HMAC
        mac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()  # 直接使用 secret_key
        macs.append(mac)
    return macs

def verify_mac(location_data, received_mac, secret_key):
    # 将位置信息转换为字符串
    message = f"{location_data[0]},{location_data[1]},{location_data[2]}".encode()
    # 重新计算 HMAC
    calculated_mac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()  # 直接使用 secret_key
    # 比较 MAC 值
    return hmac.compare_digest(calculated_mac, received_mac)
