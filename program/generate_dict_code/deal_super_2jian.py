import os
import string


jianpin_word_map = {}
file_list = ['base.dict.yaml','ext.dict.yaml']
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

file_path = "custom_phrase/custom_phrase_super_2jian.txt"
with open(file_path, "w") as file:
    file.write("## 超强2简 26*26=676词空间。 使用deal_super_2jian.py生成\n")
# 遍历字符串序列
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
            if word == '但是':
                word = '都是'
            if word == '现在':
                word = '选择'
            if word == '所以':
                word = '所有'
            if word == '认为':
                word = '让我'
            if word == '自己':
                word = '最近'
            if word == '目前':
                word = '明确'
            if word == '只是':
                word = '知识'
            if word == '不再':
                word = '不在'
            if word == '受到':
                word = '收到'
            if word == '感觉':
                word = '国家'
            if word == '过去':
                word = '感情'
            if word == '认真':
                word = '日志'
            if word == '申请':
                word = '失去'
            if word == '准备':
                word = '这边'
            
            if combination == 'jq':
                word = '机器'
            if combination == 'yi':
                word = '异常'
            if combination == 'vr':
                word = '主任'
            if combination == 'vw':
                word = '职位'
            if combination == 'xl':
                word = '心理'
            if combination == 'yp':
                word = '一篇'
            if combination == 'um':
                word = '上面'
            if combination == 'fz':
                word = '否则'
            if combination == 'qu':
                word = '确实'
            if combination == 'eq':
                word = '二区'
            if combination == 'pu':
                word = '评审'
            if combination == 'xd':
                word = '许多'
            if combination == 'nm':
                word = '你们'
            if combination == 'my':
                word = '满意'
            if combination == 'yb':
                word = '一遍'
            if combination == 'yv':
                word = '一种'
            if combination == 'zm':
                word = '咱们'
            if combination == 'fx':
                word = '分享'
            if combination == 'av':
                word = '安装'
            if combination == 'vm':
                word = '专门'
            if combination == 'gg':
                word = '哥哥'
            if combination == 'vn':
                word = '智能'
            file.write(word+"\t"+combination+"/\n")
            # print(combination + " " + str(word_freq_list))
        # print(combination + jianpin_word_map[combination])