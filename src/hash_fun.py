import hashlib



def generate_hash_functions(ga_ma):
    """
    生成无偏哈希函数集
    :param ga_ma: 哈希函数的数量
    :return: 哈希函数列表
    """
    hash_functions = []
    for i in range(ga_ma):
        def hash_function(x, seed=i):
            # 使用 sha256 作为无偏哈希函数
            return int(hashlib.sha256((str(seed) + x).encode()).hexdigest(), 16)
        hash_functions.append(hash_function)
    return hash_functions

