import os


def write_to_file_as_list(filename, data):
    """
    将给定的数据写入 E:\experi\output 文件夹中的文件，并将内容格式化为列表的形式。
    """
    # 直接指定完整路径
    output_dir = r"E:\experi\output"

    # 如果 output 文件夹不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"文件夹 {output_dir} 已创建")

    # 生成完整的文件路径
    file_path = os.path.join(output_dir, filename)


    try:
        with open(file_path, 'w') as f:
            # 模拟列表格式输出
            f.write("[")
            f.write(", ".join(map(str, data)))
            f.write("]\n")
        #print(f"数据已成功写入 {file_path}")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")



