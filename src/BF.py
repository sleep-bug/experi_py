
import os
import random

from SHE import Encryption, KeyGen
from config import set_pp_sk_H, set_k, set_pk, set_ga_ma, set_m
from file_operations import write_to_file_as_list



class BloomFilter:
    def __init__(self, hash_functions, size):
        self.size = size
        self.bit_array = [0] * size
        self.hash_functions = hash_functions

    def add(self, item):
        for i, hash_func in enumerate(self.hash_functions):
            hash_value = hash_func(item)
            index = hash_value % self.size

            self.bit_array[index] = 1  # 更新bit_array对应索引的位置为1


    def check(self, item):
        for hash_func in self.hash_functions:
            index = hash_func(item) % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    def encrypt_bitarray(self, pk):
        """
        对布隆过滤器的位数组中的每一位进行加密。
        """
        pp, _ = set_pp_sk_H()
        encrypted_bits = []
        for bit in self.bit_array:
            encrypted_bits.append(Encryption(bit, pk, pp))
        return encrypted_bits

    def generate_perturbations(self):
        """
        生成与布隆过滤器位数组大小相同的干扰值数组。
        """
        perturbations = [random.randint(1, 9) for _ in range(self.size)]  # 使用列表存储1到9之间的整数
        return perturbations

    def add_perturbations(self, filename):
        """
        将生成的干扰值添加到布隆过滤器的位数组。
        """
        perturbations = self.generate_perturbations()
        #print(f"干扰值是: {perturbations}")
        full_path = os.path.join(r"E:\experi\output\perturbations", filename)
        write_to_file_as_list(full_path, perturbations)

        # 生成新的位数组，将原始位数组与干扰值相加，保留结果
        perturbed_bit_array = [self.bit_array[i] + perturbations[i] for i in range(self.size)]

        return perturbed_bit_array, perturbations


