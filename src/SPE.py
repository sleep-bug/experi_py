import math

from sympy.diffgeom import twoform_to_matrix


def compute_z_order(x, y):

    max_val = max(x, y)
    bit_length = max_val.bit_length()

    # Convert x and y to binary, and pad with leading zeros
    x_bin = format(x, f'0{bit_length}b')
    y_bin = format(y, f'0{bit_length}b')

    # Interleave bits of x and y to form the Z-order code
    z_order = []
    for i in range(bit_length):
        z_order.append(x_bin[i])
        z_order.append(y_bin[i])

    return ''.join(z_order)


def get_bit_length(points):
    max_val = max(max(x, y) for x, y in points)
    return max_val.bit_length()


def encodearea(points):
    # Compute Z-order for all points
    z_orders = [compute_z_order(x, y) for x, y in points]

    # Find valid prefixes using the previous logic
    valid_prefixes, no_valid_prefixes = find_common_prefixes(z_orders)

    return z_orders, valid_prefixes, no_valid_prefixes


def find_common_prefixes(binary_strings):
    n = len(binary_strings)
    max_length = max(len(s) for s in binary_strings)

    valid_prefixes = []
    no_valid_prefixes = set(binary_strings)

    for length in range(2, max_length + 1, 2):
        prefix_dict = {}

        for s in binary_strings:
            prefix = s[:length]
            quadrant_key = s[length:length + 2]
            if prefix not in prefix_dict:
                prefix_dict[prefix] = set()
            prefix_dict[prefix].add(quadrant_key)

        for prefix, quadrants in prefix_dict.items():
            if {'00', '01', '10', '11'}.issubset(quadrants):
                valid_prefixes.append(prefix)
                no_valid_prefixes.difference_update([s for s in binary_strings if s.startswith(prefix)])

    return valid_prefixes, list(no_valid_prefixes)

def encodeloc(z_order_code):
    # 初始化集合
    F_set = set()

    # 从完整的Z-order编码开始
    for i in range(0, len(z_order_code), 2):  # 每次删除两位
        F_set.add(z_order_code[:len(z_order_code) - i])

    return F_set


# 检查交集是否存在
def has_intersection(S, F_p_i):
    return len(S & F_p_i) > 0


