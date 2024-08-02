import os
import re
import string

# 对比一下小鹤的2字词
file_name = os.path.join('cn_dicts_dazhu', "flypy.yaml")
write_file_name = os.path.join('cn_dicts_dazhu', "flypy_word.yaml")
write_file = open(write_file_name, 'w')
with open(file_name, 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 去除行尾的换行符
        line = line.rstrip()
        if '\t' not in line:
            continue
        params = line.split("\t")
        word = params[0]
        encode = params[1]
        if len(word) != 2:
            continue
        if len(encode) != 4:
            continue
        write_file.write(line+"\n")