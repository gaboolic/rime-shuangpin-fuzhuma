import os

dict_data = {}
with open('./opencc/moqi_chaifen.txt', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if "\t" in line:
            character, encoding, chaifen = line.strip().split('\t')
            if "'" not in encoding:
                
                # if character in '去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗':
                #     encoding = encoding[0] + encoding[1].upper()
                if character not in dict_data:
                    dict_data[character] = encoding


print("巴 " + dict_data['巴'])
print("𬱖 " + dict_data['𬱖'])

# 写入多行数据到文件
with open('cn_dicts_dazhu/chaifen=.txt', 'w') as file:
    
    for key in dict_data:
        line = f"{key}={dict_data[key]}"
        print(line)
        file.write(line)
        file.write("\n")
