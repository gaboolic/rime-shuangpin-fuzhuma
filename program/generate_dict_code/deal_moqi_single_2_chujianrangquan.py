import os
import re

write_file = open('cn_dicts_dazhu/4code.txt', 'w', encoding='utf-8')
# 4码的 生成出简让全
code_4_char_list = []
with open('moqi_single.dict.yaml', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')
        code = params[1]
        if len(code)!= 4:
            continue
        
        if code not in code_4_char_list:
            code_4_char_list.append(code)
            write_file.write(params[0]+"\t"+params[1]+"/\n")
        
