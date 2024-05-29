import os
import re

char_list = {}
encode_count_map = {}
file_list = ['8105.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml','41448.dict.yaml']
# file_list = ['41448.dict.yaml']
# file_list = [ 'tencent.dict.yaml']
# Load the dict data from the provided file

def read_file(file_path):
    list = []
    with open(file_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if not '\t' in line or line.startswith("#"):
                continue
            

            params = line.split('\t');
            if params[1] == "100":
                continue

            character = params[0]
            encoding = params[1]

            encoding = re.sub(r'\[', '', encoding)
            pinyin_list = encoding.split(" ")
            new_encoding2 = ""
            for pinyin in pinyin_list:
                pinyin = pinyin[0:2]
                new_encoding2 += pinyin

            new_encoding3 = new_encoding2
            new_encoding4 = new_encoding2
            if len(pinyin) > 2:
                for pinyin in pinyin_list:
                    pinyin = pinyin[0:3]
                    new_encoding3 += pinyin
                for pinyin in pinyin_list:
                    pinyin = pinyin[0:4]
                    new_encoding4 += pinyin
            
            
            
            if new_encoding2 not in encode_count_map or encode_count_map[new_encoding2] < 4:
                encoding = new_encoding2
            elif new_encoding3 not in encode_count_map or encode_count_map[new_encoding3] < 4:
                encoding = new_encoding3
            else:
                encoding = new_encoding4
            
            if encoding not in encode_count_map:
                encode_count_map[encoding] = 1
            else:
                encode_count_map[encoding] += 1
            

            if character in char_list:
                pass
            else:
                char_list[character] = 1
                # list.append(f"{character}\t{encoding}")
                list.append(f"{encoding}\t{character}")
    return list

final_list = []
for file_name in file_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_moqi', file_name)

    for line in read_file(yaml_file_path):
        final_list.append(line)

# 写入多行数据到文件
with open('cn_dicts_dazhu/moqi_all.txt', 'w') as file:
    file.writelines('\n'.join(final_list))