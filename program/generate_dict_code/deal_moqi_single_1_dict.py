import os
import re

char_list = {}
encode_count_map = {}
file_list = ['8105.dict.yaml']
# file_list = ['41448.dict.yaml']
# file_list = [ 'tencent.dict.yaml']
# Load the dict data from the provided file

# 3码的 生成出简让全
phrase_code_2_map = {}
with open('custom_phrase/custom_phrase.txt', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')
        # print(params)
        if len(params[1])==2 and len(params[0]) == 1:
            phrase_code_2_map[params[0]] = params[1]
            pass

def custom_sort(word_freq):
    special_words = "去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗"
    # 如果当前词是特定字，则将其排在最前面
    line = word_freq['line']
    params = line.split('\t');
    encoding = params[1]
    encoding = re.sub(r'\[', '', encoding)
    pinyin = encoding[0:2]
    if word_freq['word'] == '的' and pinyin != 'de':
        return (2, -int(word_freq['freq']))  # 其他词按照频率降序排列
    if word_freq['word'] == '哦' and pinyin != 'oo':
        return (2, -int(word_freq['freq']))  # 其他词按照频率降序排列
    if word_freq['word'] == '和' and pinyin != 'he':
        return (2, -int(word_freq['freq']))  # 其他词按照频率降序排列
    if word_freq['word'] == '了' and pinyin != 'le':
        return (2, -int(word_freq['freq']))  # 其他词按照频率降序排列
    
    # 2码字 优先级为1
    if word_freq['word'] in phrase_code_2_map and phrase_code_2_map[word_freq['word']] == pinyin:
        return (1, -int(word_freq['freq']))  # 其他词按照频率降序排列

    if word_freq['word'] in special_words:
        return (0, -int(word_freq['freq']))  # 将特定字排在最前面并按频率降序排列
    else:
        return (2, -int(word_freq['freq']))  # 其他词按照频率降序排列




jianpin_word_map = {}
def read_file(file_path):
    list = []

    with open(file_path, 'r', encoding='utf-8') as dict_file:
        for line in dict_file:
            if not '\t' in line or line.startswith("#"):
                continue
            line = line.strip()
            params = line.split('\t');

            character = params[0]
            encoding = params[1]
            encoding = re.sub(r'\[', '', encoding)
            pinyin = encoding[0:2]
            freq = params[2]
            word_freq = {}
            word_freq["word"] = character
            word_freq["freq"] = freq
            word_freq["line"] = line

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
        word_freq_list = sorted(word_freq_list, key=custom_sort)
        # word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)
        if combination == 'le':
            # print(combination)
            # print(word_freq_list)
            pass

        for word in word_freq_list:
            line = word['line']
            params = line.split('\t')

            character = params[0]
            encoding = params[1]

            encoding = re.sub(r'\[', '', encoding)

            new_encoding1 = encoding[0:1]
            new_encoding2 = encoding[0:2]
            pinyin = new_encoding2
            new_encoding3 = encoding[0:3]
            new_encoding4 = encoding[0:4]
            
            #排除26个1简
            if character in "去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗":
                if character == '了' and pinyin != 'le':
                    pass
                elif character == '的' and pinyin != 'de':
                    pass
                elif character == '哦' and pinyin != 'oo':
                    pass
                elif character == '和' and pinyin != 'he':
                    pass
                else:
                    char_list[character+new_encoding1] = re.sub(r'\[', '', params[1])
                    continue
            
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
            
            char_list[character+pinyin] = re.sub(r'\[', '', params[1])
            
            list.append(f"{character}\t{encoding}")
    return list

final_code_char_map = {}
final_list = []
write_file = open('cn_dicts_dazhu/moqi_all2.txt', 'w')
for file_name in file_list:
    # File paths
    yaml_file_path = os.path.join('cn_dicts_moqi', file_name)

    read_file_lines = read_file(yaml_file_path)
    #print(read_file_lines)
    for line in read_file_lines:
        params = line.split("\t")
        final_code_char_map[params[1]] = params[0]
        if len(params[1])==2:
            # print(line)
            write_file.write(line+"\n")
            pass
        final_list.append(line)

# 写入多行数据到文件
with open('cn_dicts_dazhu/moqi_all.txt', 'w') as file:
    file.write("""去	q
我	w
而	e
人	r
他	t
有	y
是	u
出	i
哦	o
配	p
啊	a
算	s
的	d
非	f
个	g
和	h
就	j
可	k
了	l
在	z
小	x
从	c
这	v
吧	b
你	n
吗	m\n""")
    file.writelines('\n'.join(final_list))
    pass

# 3码的 生成出简让全
code_2_char_list = []
with open('cn_dicts_dazhu/moqi_all.txt', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')
        print(params[1])
        if len(params[1])==2 or len(params[1])==1:
            code_2_char_list.append(params[0]+params[1])
            pass

print(code_2_char_list)
code_3_file = open("custom_phrase/custom_phrase_3_code.txt", "w")
code_3_file.write("她	ta	1\n")
for code_2_char in code_2_char_list:
    all_code = char_list[code_2_char]
    code_3 = all_code[0:3]
    
    if code_3 in final_code_char_map:
        # print(final_code_char_map[code_3]+"\t"+code_3)
        code_3_file.write(final_code_char_map[code_3]+"\t"+code_3+"\n")