import os
import string

# 4码 2字词

# 生成 'aaaa' 到 'zzzz' 的字符串序列
combinations = []

for i in range(ord('a'), ord('z')+1):
    for j in range(ord('a'), ord('z')+1):
        for k in range(ord('a'), ord('z')+1):
            for l in range(ord('a'), ord('z')+1):
                combinations.append(chr(i) + chr(j) + chr(k) + chr(l))




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
            
            if len(word) != 2:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            if len(shengmus) != 2:
                continue
            jianpin = shengmus[0][0] +shengmus[0][1] +shengmus[1][0]+shengmus[1][1]

            word_freq = {}
            word_freq["word"] = word
            word_freq["freq"] = freq

            if int(freq) < 1:
                continue
            if jianpin not in jianpin_word_map:
                word_list = []
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list
            else:
                word_list = jianpin_word_map[jianpin]
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list

print(jianpin_word_map)



file_path = os.path.join('cn_dicts_moqi', 'word.dict.yaml')

with open(file_path, "w") as file:
    file.write("""## 4码 2字词 使用deal_4code_word.py生成
---
name: word
version: "2024-06-05"
sort: by_weight
...""")
    file.write("\n")
    file.write("## 4码 2字词 使用deal_4code_word.py生成\n")
                

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