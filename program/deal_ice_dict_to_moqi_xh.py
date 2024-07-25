import os
from collections import OrderedDict

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# Function to update missing encodings in the file
def update_missing_encodings(file_path, write_file_path, dict_data):
    # Read the file content
    file_content = read_file(file_path)

    # Split the content into lines
    lines = file_content.split('\n')

    # Create an updated content variable
    updated_content = ''

    # Process each line
    for line in lines:
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue

        frequency = None
         # 检查分割出的值是否足够
        if len(line.split('\t')) == 3:
            character, encoding, frequency = line.split('\t')
        else:
            character, encoding = line.split('\t')
        
        if "tencent" in file_path :
            updated_line = f"{character}\t99"
            updated_content += updated_line + '\n'
            continue
        else:
            if encoding == "100":
                updated_content += line + '\n'
                continue

        pinyin_list = encoding.split(" ")
        double_list = ""
        pinyin_index = 0
        #print(line)
        for pinyin in pinyin_list:
            if len(pinyin) == 2:
                double_pinyin = pinyin
            elif len(pinyin) == 1:
                double_pinyin = pinyin + pinyin
            else:
                shengmu = pinyin[0]
                yunmu = pinyin[1:]

                double_shengmu = shengmu
                if pinyin[1] == "h":
                    shengmu = pinyin[:2]
                    yunmu = pinyin[2:]
                    shengmu_map = { "zh": "v", "ch": "i", "sh": "u" }
                    double_shengmu = shengmu_map[shengmu]
                
                if double_shengmu == 'a':
                    yunmu = pinyin
                
                if double_shengmu == 'o':
                    yunmu = pinyin
                
                if double_shengmu == 'e':
                    yunmu = pinyin
                
                yunmu_map = {
                    'iu': 'q',
                    'ei': 'w',
                    'uan': 'r',
                    'van': 'r',

                    'ue': 't',
                    've': 't',
                    'un': 'y',
                    'vn': 'y',
                    'uo': 'o',
                    'ie': 'p',

                    'iong': 's',
                    'ong': 's',

                    'ai': 'd',
                    'en': 'f',

                    'eng': 'g',
                    'ang': 'h',
                    'an': 'j',

                    'ing': 'k',
                    'uai': 'k',
                    'iang': 'l',
                    'uang': 'l',

                    'ou': 'z',
                    'ia': 'x',
                    'ua': 'x',
                    'ao': 'c',
                    'ui': 'v',
                    'in': 'b',

                    'iao': 'n',

                    'ian': 'm',
                };
                
                if len(yunmu) == 1:
                    double_yummu = yunmu
                else:
                    double_yummu = yunmu_map[yunmu]
                double_pinyin = double_shengmu + double_yummu

                if len(double_pinyin) != 2:
                    print("!!!!double_pinyin " + double_pinyin + " " + pinyin + " ")
                
            clean_character = character.replace("·", "")
            #print(line)
            character_encoding_pre = clean_character[pinyin_index]
            # character_encoding_pre = character[pinyin_index]
            encoding_post = dict_data.get(character_encoding_pre, "[")
            double_list += f"{double_pinyin}[{encoding_post} "
            pinyin_index += 1
        
        double_list = double_list[:-1]

        if "[[" in double_list:
            # updated_content += line + '\n'
            pass

        if "tencent" in file_path :
            updated_line = f"{character}\t99"
        else:
            if frequency is not None:
                updated_line = f"{character}\t{double_list}\t{frequency}"
            else :
                updated_line = f"{character}\t{double_list}"
        updated_content += updated_line + '\n'

    # Write the updated content back to the file
    write_file(write_file_path, updated_content)

dict_data = {}
file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
# file_list = [ 'tencent.dict.yaml']
# Load the dict data from the provided file
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
print("㪱 " + dict_data['㪱'])

for file_name in file_list:
    # File paths
    cn_dicts_path = os.path.expanduser("~/vscode/rime-frost/cn_dicts")
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts_moqi', file_name)

    print(yaml_file_path)
    # Update missing encodings in the file
    update_missing_encodings(yaml_file_path, write_file_path, dict_data)

# 聚合细胞词库
frost_cell_dict_path = os.path.expanduser("~/vscode/rime-frost/cn_dicts_cell")
# 使用 os 模块中的 listdir 函数列出指定文件夹中的所有文件和子目录
cell_file_names = os.listdir(frost_cell_dict_path)
word_map = OrderedDict()
for file_name in cell_file_names:
    read_file_name = os.path.join(os.path.expanduser("~/vscode/rime-frost/cn_dicts_cell"), file_name)
    #print(read_file_name)
    
    with open(read_file_name, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 去除行尾的换行符
            line = line.rstrip()
            if line.startswith('#') or '\t' not in line:
                continue
            params = line.split("\t")
            word = params[0]
            encode = params[1]
            
            key = word + encode
            if key not in word_map:
                word_map[line]=''
    
write_cell_file_name = os.path.join('cn_dicts_dazhu', 'cell.dict.yaml')
write_cell_file = open(write_cell_file_name, 'w')
write_cell_file.write("""# Rime dictionary
# encoding: utf-8
# 细胞词库 来自https://github.com/gaboolic/rime-frost/tree/master/cn_dicts_cell
---
name: cell
version: "2024-07-17"
sort: by_weight
...
# +_+
""")
for word in word_map:
    write_cell_file.write(word+"\n")
write_cell_file.close()

yaml_file_path = os.path.join('cn_dicts_dazhu', 'cell.dict.yaml')
write_file_path = os.path.join('cn_dicts_moqi', 'cell.dict.yaml')

print(yaml_file_path)
# Update missing encodings in the file
update_missing_encodings(yaml_file_path, write_file_path, dict_data)