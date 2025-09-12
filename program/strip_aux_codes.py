import os

# 读取文件的函数
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 写入内容到文件的函数
def write_file(file_path, content):
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# 从词典文件中移除辅助码的函数
def update_missing_encodings(file_path, write_file_path, dict_data=None):
    # 读取文件内容
    print(f"处理文件: {file_path}")
    file_content = read_file(file_path)

    # 将内容分割成行
    lines = file_content.split('\n')

    # 创建更新后的内容变量
    updated_content = ''

    print(f"总行数: {len(lines)}")
    # 处理每一行
    for line in lines:
        # 跳过注释和没有制表符分隔的行
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue

        # 提取字符、编码和频率（如果存在）
        frequency = None
        if len(line.split('\t')) == 3:
            character, encoding, frequency = line.split('\t')
        else:
            character, encoding = line.split('\t')

        # 腾讯特殊处理（如果需要）
        if "tencent" in file_path:
            updated_line = f"{character}\t99"
            updated_content += updated_line + '\n'
            continue
        else:
            if encoding == "100":
                updated_content += line + '\n'
                continue

        # 处理编码：提取分号前的拼音部分
        pinyin_list = encoding.split(" ")
        clean_pinyins = []
        
        for pinyin_part in pinyin_list:
            # 按分号分割，取第一部分（纯拼音）
            if ';' in pinyin_part:
                clean_pinyin = pinyin_part.split(';')[0]
                clean_pinyins.append(clean_pinyin)
            else:
                # 如果没有分号，保持原样
                clean_pinyins.append(pinyin_part)
        
        # 合并干净的拼音
        clean_encoding = " ".join(clean_pinyins)
        
        # 创建更新行，包含或不包含频率
        if frequency is not None:
            updated_line = f"{character}\t{clean_encoding}\t{frequency}"
        else:
            updated_line = f"{character}\t{clean_encoding}"
        
        updated_content += updated_line + '\n'

    # 将更新后的内容写回文件
    print(f"写入到: {write_file_path}")
    write_file(write_file_path, updated_content)
    print("处理完成。")

# 如果直接运行此脚本，则执行以下代码
if __name__ == "__main__":
    # 获取当前文件所在目录的父目录（项目根目录）
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 示例：处理8105.dict.yaml文件
    file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
    for file_name in file_list:
        # 文件路径
        cn_dicts_path = os.path.join(root_path, "cn_dicts")
        yaml_file_path = os.path.join(cn_dicts_path, file_name)
        write_file_path = os.path.join('cn_dicts', file_name)

        print(yaml_file_path)
        # 更新文件中的缺失编码
        update_missing_encodings(yaml_file_path, write_file_path, None)

    # 细胞词库
    cell_path =  os.path.join(root_path, "cn_dicts_cell")
    for file_name in os.listdir(cell_path):
        # 文件路径
        cn_dicts_path = cell_path
        yaml_file_path = os.path.join(cn_dicts_path, file_name)
        write_file_path = os.path.join('cn_dicts_cell', file_name)

        print(yaml_file_path)
        # 更新文件中的缺失编码
        update_missing_encodings(yaml_file_path, write_file_path, None)
