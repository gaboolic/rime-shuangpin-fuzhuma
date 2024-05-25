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
            
            if len(word) != 2:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] + shengmus[1][0]

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


# 生成 'aa' 到 'az' 的字符串序列
letters = string.ascii_lowercase
combinations = [a + b for a in letters for b in letters]

# 遍历字符串序列
for combination in combinations:
    if combination not in jianpin_word_map:
        print(combination)
    else:
        word_freq_list = jianpin_word_map[combination]
        # 对字典列表进行排序
        word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)

        # 取出前三个元素
        word_freq_list = word_freq_list[:3]
        word = word_freq_list[0]['word']
        print(word+"\t"+combination+"|")
        # print(combination + " " + str(word_freq_list))
    # print(combination + jianpin_word_map[combination])