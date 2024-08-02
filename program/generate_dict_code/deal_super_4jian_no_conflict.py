import os
import string


jianpin_word_map = {}
file_list = ['8105.dict.yaml','41448.dict.yaml']
for file in file_list:
    file_name  = os.path.join('cn_dicts_moqi', file)
    with open(file_name, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 去除行尾的换行符
            line = line.rstrip()
            if line.startswith('#') or '\t' not in line:
                continue
            params = line.split("\t")
            word = params[0]
            
            if len(word) != 1:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] +shengmus[0][1] +shengmus[0][3]+shengmus[0][4]
            word_freq = {}
            word_freq["word"] = word
            if jianpin not in jianpin_word_map:
                word_list = []
                word_list.append(word)
                jianpin_word_map[jianpin] = word_list
            else:
                word_list = jianpin_word_map[jianpin]
                word_list.append(word)
                jianpin_word_map[jianpin] = word_list

file_list = ['base.dict.yaml','ext.dict.yaml']
for file in file_list:
    file_name  = os.path.join('cn_dicts_moqi', file)
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
            if int(freq) < 998:
                continue
            if len(word) != 2:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] +shengmus[0][1] +shengmus[1][0]+shengmus[1][1]
            word_freq = {}
            word_freq["word"] = word
            if jianpin not in jianpin_word_map:
                word_list = []
                word_list.append(word)
                jianpin_word_map[jianpin] = word_list
            else:
                word_list = jianpin_word_map[jianpin]
                word_list.append(word)
                jianpin_word_map[jianpin] = word_list



# 生成 'aaaa' 到 'zzzz' 的字符串序列
combinations = []

for i in range(ord('a'), ord('z')+1):
    for j in range(ord('a'), ord('z')+1):
        for k in range(ord('a'), ord('z')+1):
            for l in range(ord('a'), ord('z')+1):
                combinations.append(chr(i) + chr(j) + chr(k) + chr(l))


no_conflict_list = []
# 遍历字符串序列
for combination in combinations:
    if combination not in jianpin_word_map:
        no_conflict_list.append(combination)

# print(no_conflict_list)

import os
import string


jianpin_word_map = {}
file_list = ['base.dict.yaml','ext.dict.yaml']
for file in file_list:
    file_name  = os.path.join('cn_dicts_moqi', file)
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
            
            if len(word) != 4:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            if len(shengmus) != 4:
                continue
            jianpin = shengmus[0][0] + shengmus[1][0] + shengmus[2][0]+ shengmus[3][0]

            word_freq = {}
            word_freq["word"] = word
            word_freq["freq"] = freq
            if jianpin not in jianpin_word_map:
                word_list = []
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list
            else:
                word_list = jianpin_word_map[jianpin]
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list

# print(jianpin_word_map)



file_path = "custom_phrase/custom_phrase_super_4jian_no_conflict.txt"

with open(file_path, "w") as file:
    file.write("## 超强4简 使用deal_super_4jian_no_conflict.py生成\n")
                

    # 遍历字符串序列
    # combinations 所有
    # no_conflict_list 不冲突
    for combination in combinations:
        if combination not in jianpin_word_map:
            # print(combination)
            pass
        else:
            word_freq_list = jianpin_word_map[combination]
            # 对字典列表进行排序
            word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)

            # 取出前三个元素
            word_freq_list = word_freq_list[:3]
            word = word_freq_list[0]['word']
            # print(word+"\t"+combination+"|")

            file.write(word+"\t"+combination + "\n")

            # print(combination + " " + str(word_freq_list))
    # print(combination + jianpin_word_map[combination])