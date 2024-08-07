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
            
            if len(word) != 3:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] + shengmus[1][0] + shengmus[2][0]

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


# 生成 'aaa' 到 'zzz' 的字符串序列
combinations = []

for i in range(ord('a'), ord('z')+1):
    for j in range(ord('a'), ord('z')+1):
        for k in range(ord('a'), ord('z')+1):
            combinations.append(chr(i) + chr(j) + chr(k))


file_path = "custom_phrase/custom_phrase_super_3jian.txt"
with open(file_path, "w") as file:
    file.write("## 超强3简 使用deal_super_3jian.py生成\n")
                

# 遍历字符串序列
    for combination in combinations:
        if combination not in jianpin_word_map:
            #print(combination)
            pass
        else:
            word_freq_list = jianpin_word_map[combination]
            # 对字典列表进行排序
            word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)

            # 取出前三个元素
            word_freq_list = word_freq_list[:1]
            for word_freq in word_freq_list:
                word = word_freq['word']
                # print(word+"\t"+combination+"|")
                if combination == 'xgl':
                    word = 'X光'
                if combination == 'txu':
                    word = 'T恤'
                if combination == 'upj':
                    word = 'U盘'
                if combination == 'bvj':
                    word = 'B站'
                if combination == 'qbi':
                    word = 'Q币'
                if combination == 'qqq':
                    word = 'QQ群'
                if combination == 'tgq':
                    word = 'TG群'
                if combination == 'kxm':
                    word = 'K线'
                if combination == 'upv':
                    word = 'UP主'
                if combination == 'wwc':
                    word = '维C'
                if combination == 'cpj':
                    word = 'C盘'
                if combination == 'kge':
                    word = 'K歌'
                if combination == 'ptu':
                    word = 'P图'
                if combination == 'uxg':
                    word = '鼠须管'
                if combination == 'xlh':
                    word = '小狼毫'
                if combination == 'vvy':
                    word = '中州韵'
                if combination == 'lbt':
                    word = '路边摊'
                if combination == 'zrm':
                    word = '自然码'
                if combination == 'xqy':
                    word = '星期一'
                if combination == 'shu':
                    word = '俗话说'
                if combination == 'ulx':
                    word = '试了下'
                if combination == 'kdd':
                    word = '空荡荡'
                if combination == 'dyz':
                    word = '多音字'
                if combination == 'urf':
                    word = '输入法'
                if combination == 'fvm':
                    word = '辅助码'
                if combination == 'agu':
                    word = 'A股'
                if combination == 'bic':
                    word = 'B超'
                file.write(word+"\t"+combination+"/" + "\n")

            # print(combination + " " + str(word_freq_list))
    # print(combination + jianpin_word_map[combination])

e_file_path = "cn_dicts_common/changcijian3.dict.yaml"
with open(e_file_path, "w") as file:
    title = """# 3字词
---
name: changcijian3
version: "2024-02-27"
sort: by_weight
...
# +_+
## 超强3简 使用deal_super_3jian.py生成\n"""
    file.write(title)
                

# 遍历字符串序列
    for combination in combinations:
        if combination not in jianpin_word_map:
            #print(combination)
            pass
        else:
            word_freq_list = jianpin_word_map[combination]
            # 对字典列表进行排序
            word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)

            # 取出前三个元素
            word_freq_list = word_freq_list[:5]
            for word_freq in word_freq_list:
                word = word_freq['word']

                file.write(word+"\te"+combination+ "\n")

            # print(combination + " " + str(word_freq_list))
    # print(combination + jianpin_word_map[combination])