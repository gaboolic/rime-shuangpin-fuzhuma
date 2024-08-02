import os
import re
import string

# mnbvc liwu_253874_com.jsonl
# file_name = os.path.join(os.path.expanduser("~/Downloads"),'undl_01.jsonl') # 通用平行
# file_name = os.path.join(os.path.expanduser("~/Downloads"),'liwu_253874_com.jsonl') # 里屋论坛
# file_name = os.path.join(os.path.expanduser("~/Downloads"),'46.jsonl') #维基
# file_name = os.path.join(os.path.expanduser("~/Downloads"),'oscar_202201.part_0075.jsonl') # 通用文本
file_name = os.path.join(os.path.expanduser("~/mnbvc"),'0.jsonl') # 知乎 https://huggingface.co/datasets/liwu/MNBVC/tree/main/qa/20230196/zhihu
write_file_name = os.path.join('cn_dicts_dazhu', "flypy_word.yaml")
write_file = open(write_file_name, 'w')
with open(file_name, 'r') as file:
    line = file.readline()
    print(line)
    print()
    line = file.readline()
    print(line)
    print()
    line = file.readline()
    print(line)
    print()
    line = file.readline()
    print(line)
    print()