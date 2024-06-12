import os
import re
import string


word_jianpin_map = {}
file_list = ['base.dict.yaml']
for file in file_list:
    file_name = os.path.join('cn_dicts_moqi', file)
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
            
            if len(word) != 2:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] + shengmus[1][0]

            word_freq = {}
            word_freq["word"] = word
            word_freq["freq"] = freq
            word_freq["jianpin"] = jianpin
            if word not in word_jianpin_map:
                word_jianpin_map[word] = word_freq

print(word_jianpin_map['什么'])

jianpin_word_map = {}

with open("program/2字词频表.txt", 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        line = line.strip()
        if not '\t' in line or line.startswith("#"):
            #list.append(line)
            continue
        line = line.strip()
        params = line.split('\t');
        
        word = params[0]
        freq = params[1]
        freq = (''.join(re.findall(r'\d+', freq)))
        if int(freq) < 3000:
            break

        if word not in word_jianpin_map:
            continue
        jianpin = word_jianpin_map[word]
        jianpin = jianpin['jianpin']
        print(jianpin)
        if jianpin not in jianpin_word_map:
            word_list = []
            word_list.append(word)
            jianpin_word_map[jianpin] = word_list
        else:
            word_list = jianpin_word_map[jianpin]
            word_list.append(word)
            jianpin_word_map[jianpin] = word_list


        #print(line)
        # list.append(f"{character}\t{encoding}")
        #list.append(f"{character}\t{encoding}\t{freq}")
print(jianpin_word_map) 
# 生成 'aa' 到 'az' 的字符串序列
letters = string.ascii_lowercase
combinations = [a + b for a in letters for b in letters]
file_path = "custom_phrase/custom_phrase_super_2jian2.txt"
with open(file_path, "w") as file:
    file.write("## 超强2简 26*26=676词空间。 使用deal_super_2jian.py生成\n")
# 遍历字符串序列
    for combination in combinations:
        if combination not in jianpin_word_map:
            # print(combination)
            pass
        else:
            word_freq_list = jianpin_word_map[combination]
            

            # 取出前三个元素
            word_freq_list = word_freq_list[:3]
            word = word_freq_list[0]
            # if word == '但是':
            #     word = '都是'
            # if word == '现在':
            #     word = '选择'
            # if word == '所以':
            #     word = '所有'
            # if word == '认为':
            #     word = '让我'
            # if word == '自己':
            #     word = '最近'
            # if word == '目前':
            #     word = '明确'
            # if word == '只是':
            #     word = '知识'
            file.write(word+"\t"+combination+"/\n")
            # print(combination + " " + str(word_freq_list))
        # print(combination + jianpin_word_map[combination])
