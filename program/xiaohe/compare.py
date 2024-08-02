import os
import re
import string


xh_code_word_map = {}
file_name = os.path.join('cn_dicts_dazhu', "flypy_word.yaml")
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
        xh_code_word_map[encode] = word
        
mq_code_word_map = {}
file_name = os.path.join('cn_dicts_moqi', "word.dict.yaml")
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
        mq_code_word_map[encode] = word
        


# 生成 'aaaa' 到 'zzzz' 的字符串序列
combinations = []

for i in range(ord('a'), ord('z')+1):
    for j in range(ord('a'), ord('z')+1):
        for k in range(ord('a'), ord('z')+1):
            for l in range(ord('a'), ord('z')+1):
                combinations.append(chr(i) + chr(j) + chr(k) + chr(l))


write_file_name = os.path.join('cn_dicts_dazhu', "diff_word.yaml")
write_file = open(write_file_name, 'w')

# 遍历字符串序列
for combination in combinations:
    if combination in xh_code_word_map and combination in mq_code_word_map:
        xh_word = xh_code_word_map[combination]
        mq_word = mq_code_word_map[combination]
        if xh_word != mq_word:
            write_file.write(f"{combination} {xh_word} {mq_word}\n")