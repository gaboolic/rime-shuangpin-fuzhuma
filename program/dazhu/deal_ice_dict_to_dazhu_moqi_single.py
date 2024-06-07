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
            # print(line)
            params = line.split('\t');
            
            character = params[0]
            encoding = params[1]

            if encoding.endswith("/"):
                encoding = encoding[:-1].upper()

            # list.append(f"{character}\t{encoding}")
            list.append(f"{encoding}\t{character}")
                
    return list


final_list = []

tab_list = ['custom_phrase.txt','custom_phrase_super_1jian.txt', 'custom_phrase_super_2jian.txt','custom_phrase_super_3jian.txt','custom_phrase_super_3jian_no_conflict.txt']
cn_dicts_common_list = ['4jian_no_conflict.dict.yaml', 'changcijian.dict.yaml']
cn_dicts_moqi_list = ['word.dict.yaml']
char_list = ['moqi_single.dict.yaml']

for file_name in tab_list:
    # File paths
    yaml_file_path = os.path.join('custom_phrase', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)

for file_name in cn_dicts_common_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_common', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)

for file_name in cn_dicts_moqi_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_moqi', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)

for file_name in char_list:
    # File paths
    yaml_file_path = os.path.join('', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)

# 写入多行数据到文件
with open('cn_dicts_dazhu/moqi_single_all.txt', 'w') as file:
    file.writelines('\n'.join(final_list))