
def remove_perturbations(bf_S_A_pri, perturbations):
    """
    从位数组中去除干扰值，恢复原始的布隆过滤器位数组。
    """
    # 确保干扰值和布隆过滤器长度相同
    if len(bf_S_A_pri) != len(perturbations):
        raise ValueError("干扰值和布隆过滤器长度不一致！")

    # 去除干扰值，保留相减结果
    for i in range(len(bf_S_A_pri)):
        bf_S_A_pri[i] = bf_S_A_pri[i] - perturbations[i]  # 不再取模，直接相减

    return bf_S_A_pri



