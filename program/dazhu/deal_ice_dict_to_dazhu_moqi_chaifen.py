import os
import re


char_list = {}
encode_count_map = {}



def read_file(file_path):
    list = []
    with open(file_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if not '\t' in line or line.startswith("#"):
                continue
            line = line.strip()
            print(line)
            params = line.split('\t');
            
            character = params[0]
            encoding = params[1]

            if "41448" in file_path:
                encoding = "双拼[辅助码："+encoding

            # list.append(f"{character}\t{encoding}")
            list.append(f"{encoding}\t{character}")
                
    return list


final_list = []

cn_dicts_common_list = [ 'moqi_chaifen_all.txt']


for file_name in cn_dicts_common_list:
    # File paths
    yaml_file_path = os.path.join('opencc', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)


cn_dicts_common_list = [ '41448.dict.yaml']
for file_name in cn_dicts_common_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_moqi', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)



# 写入多行数据到文件
with open('cn_dicts_dazhu/moqi_chaifen_all.txt', 'w') as file:
    file.writelines('\n'.join(final_list))