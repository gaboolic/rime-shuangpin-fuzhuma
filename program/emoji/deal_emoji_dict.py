import os
import string


word_pinyin_map = {}
file_list = ['8105.dict.yaml','base.dict.yaml','ext.dict.yaml']
for file in file_list:
    file_name = os.path.join('cn_dicts', file)
    with open(file_name, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 去除行尾的换行符
            line = line.rstrip()
            if line.startswith('#') or '\t' not in line:
                continue
            params = line.split("\t")
            word = params[0]
            freq = params[2]
            
            pinyin = params[1]
            pinyin = pinyin.replace(" ","'")
            word_pinyin_map[word] = pinyin

# print(word_pinyin_map)
print(word_pinyin_map['人民币'])


write_file = open('emoji.dict.yaml', 'w')
title = """# 使用opencc/emoji.txt数据转换
# 转换脚本为https://github.com/gaboolic/rime-shuangpin-fuzhuma/program/emoji/deal_emoji_dict.py
# 

---
name: emoji
version: "2024-05-26"
sort: by_weight
use_preset_vocabulary: false
columns:
  - text
  - code
  - weight
...
"""
write_file.write(title+"\n")
with open("opencc/emoji.txt", 'r') as file:
    for line in file:
        # 去除行尾的换行符
        line = line.rstrip()
        if line.startswith('#') or '\t' not in line:
            continue

        params = line.split("\t")
        word = params[0]
        emojis = params[1].split(" ")
        emojis = emojis[1:]
        print(word)
        print(emojis)
        for emoji in emojis:
            content = ""
            if word not in word_pinyin_map:
                content = emoji+"\t"+word
            else:
                pinyin = word_pinyin_map[word]
                content = emoji+"\t"+pinyin
            write_file.write(content+"\n")

with open("opencc/others.txt", 'r') as file:
    for line in file:
        # 去除行尾的换行符
        line = line.rstrip()
        if not line.startswith('V') or '\t' not in line:
            continue

        params = line.split("\t")
        word = params[0]
        word = word[1:]
        emojis = params[1].split(" ")
        emojis = emojis[1:]
        print(word)
        print(emojis)
        for emoji in emojis:
            content = ""
            if word not in word_pinyin_map:
                content = emoji+"\t"+word
            else:
                pinyin = word_pinyin_map[word]
                content = emoji+"\t"+pinyin
            write_file.write(content+"\n")
            
