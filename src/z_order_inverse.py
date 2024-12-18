
# z-order的逆操作
def z_order_inverse(p):

    bin_x = bin(p)[2:]
    if len(bin_x) % 2 != 0:
        bin_x = '0' + bin_x

    part1 = ''.join(bin_x[i] for i in range(0, len(bin_x), 2))  # Even indices
    part2 = ''.join(bin_x[i] for i in range(1, len(bin_x), 2))  # Odd indices

    num1 = int(part1, 2)
    num2 = int(part2, 2)

    return (num1, num2)


'''# Test with x = 9416
x = 9416
num1 = z_order_inverse(x)
print(num1)'''
