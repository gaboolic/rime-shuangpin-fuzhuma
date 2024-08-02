import os
import re
import string

# 对比一下小鹤的2字词
file_name = os.path.join('cn_dicts_dazhu', "flypy.yaml")
write_file_name = os.path.join('cn_dicts_dazhu', "flypy_word_3zi.yaml")
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
        if len(word) != 3:
            continue
        write_file.write(line+"\n")
write_file.close()


# xh_3zi_file = open(write_file_name, 'r')
mq_3zi_file = os.path.join('custom_phrase', "custom_phrase_super_3jian.txt")
xh_3zi_map = {}
with open(write_file_name, 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 去除行尾的换行符
        line = line.rstrip()
        if '\t' not in line:
            continue
        params = line.split("\t")
        word = params[0]
        xh_3zi_map[word] = 1

mq_3zi_map = {}
with open(mq_3zi_file, 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 去除行尾的换行符
        line = line.rstrip()
        if '\t' not in line:
            continue
        params = line.split("\t")
        word = params[0]
        mq_3zi_map[word] = 1

write_file_name = os.path.join('cn_dicts_dazhu', "3字词不同.yaml")
write_file = open(write_file_name, 'w')
for xh_3 in xh_3zi_map:
    if xh_3 not in mq_3zi_map:
        print(xh_3)
        write_file.write(xh_3+"\n")