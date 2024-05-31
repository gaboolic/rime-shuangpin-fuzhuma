import os
import re

char_list = {}
encode_count_map = {}
file_list = ['8105.dict.yaml']
# file_list = ['41448.dict.yaml']
# file_list = [ 'tencent.dict.yaml']
# Load the dict data from the provided file

def custom_sort(word_freq):
    special_words = "去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗"
    # 如果当前词是特定字，则将其排在最前面
    if word_freq['word'] in special_words:
        return (0, -int(word_freq['freq']))  # 将特定字排在最前面并按频率降序排列
    else:
        return (1, -int(word_freq['freq']))  # 其他词按照频率降序排列




jianpin_word_map = {}
def read_file(file_path):
    list = []

    with open(file_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if not '\t' in line or line.startswith("#"):
                continue
            params = line.split('\t');

            character = params[0]
            encoding = params[1]
            encoding = re.sub(r'\[', '', encoding)
            pinyin = encoding[0:2]
            freq = params[2]
            word_freq = {}
            word_freq["word"] = character
            word_freq["freq"] = freq

            if pinyin not in jianpin_word_map:
                word_list = []
                word_list.append(word_freq)
                jianpin_word_map[pinyin] = word_list
            else:
                word_list = jianpin_word_map[pinyin]
                word_list.append(word_freq)
                jianpin_word_map[pinyin] = word_list

    # print(jianpin_word_map)
    # 生成 'aa' 到 'zz' 的字符串序列
    combinations = []

    for i in range(ord('a'), ord('z')+1):
        for j in range(ord('a'), ord('z')+1):
            combinations.append(chr(i) + chr(j))
    for combination in combinations:
        if combination not in jianpin_word_map:
            #print(combination)
            continue
        word_freq_list = jianpin_word_map[combination]
        # 对字典列表进行排序
        # 对字典列表进行排序
        word_freq_list = sorted(word_freq_list, key=custom_sort)
        # word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)
        if combination == 'ba':
            print(combination)
            print(word_freq_list)

    with open(file_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if not '\t' in line or line.startswith("#"):
                continue
            params = line.split('\t');

            character = params[0]
            encoding = params[1]

            encoding = re.sub(r'\[', '', encoding)
            pinyin_list = encoding.split(" ")
            new_encoding2 = ""
            for pinyin in pinyin_list:
                pinyin = pinyin[0:2]
                new_encoding2 = pinyin

            # print(pinyin)

            new_encoding3 = new_encoding2
            new_encoding4 = new_encoding2
            
            for pinyin in pinyin_list:
                pinyin = pinyin[0:3]
                new_encoding3 = pinyin
            for pinyin in pinyin_list:
                pinyin = pinyin[0:4]
                new_encoding4 = pinyin
            
            if new_encoding2 not in encode_count_map or encode_count_map[new_encoding2] < 1:
                encoding = new_encoding2
            elif new_encoding3 not in encode_count_map or encode_count_map[new_encoding3] < 1:
                encoding = new_encoding3
            else:
                encoding = new_encoding4
            
            if encoding not in encode_count_map:
                encode_count_map[encoding] = 1
            else:
                encode_count_map[encoding] += 1
            
            # print(encode_count_map)
            if character in char_list:
                pass
            else:
                char_list[character] = 1
                list.append(f"{character}\t{encoding}")
                #list.append(f"{encoding}\t{character}")
    return list

final_list = []
write_file = open('cn_dicts_dazhu/moqi_all2.txt', 'w')
for file_name in file_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_moqi', file_name)

    read_file_lines = read_file(yaml_file_path)
    #print(read_file_lines)
    for line in read_file_lines:
        params = line.split("\t")
        if len(params[1])==2:
            #print(line)
            #write_file.write(line+"\n")
            pass
        final_list.append(line)

# 写入多行数据到文件
with open('cn_dicts_dazhu/moqi_all.txt', 'w') as file:
    file.writelines('\n'.join(final_list))
    pass