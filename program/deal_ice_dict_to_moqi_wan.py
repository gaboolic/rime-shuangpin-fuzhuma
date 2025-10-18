import os
from collections import OrderedDict, defaultdict

root_path = "D:\\vscode_proj\\rime-frost"

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    if encoding not in dict_data[character]:
                        dict_data[character].append(encoding)
    return dict_data

def get_shouxin_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "=" not in line:
                    continue
                params = line.strip().split('=')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    if encoding not in dict_data[character]:
                        dict_data[character].append(encoding)
    return dict_data

def get_xh_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    encoding_post = encoding[2:]
                    if encoding_post not in dict_data[character]:
                        dict_data[character].append(encoding_post)
    return dict_data

def get_zrm_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    encoding_post = encoding[3:]
                    if encoding_post not in dict_data[character]:
                        dict_data[character].append(encoding_post)
    return dict_data

def get_shoumo_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                params = line.split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    shoumo_encode = encoding[0] + encoding[-1]
                    if shoumo_encode not in dict_data[character]:
                        dict_data[character].append(shoumo_encode)
    return dict_data

def get_pre2_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    encoding_pre = encoding[:2]
                    if encoding_pre not in dict_data[character]:
                        dict_data[character].append(encoding_pre)
    return dict_data

def get_hu_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if encoding.startswith('〔') and encoding.endswith('〕'):
                    encoding = encoding[1:-1]
                    encodeings = encoding.split("&nbsp;·&nbsp;")
                    if len(encodeings) < 2:
                        continue
                    chaifen = encodeings[0]
                    all_code = encodeings[1]
                    
                    if len(chaifen) == 1:
                        shoumo = all_code[0] + all_code[-1]
                    else:
                        shoumo = all_code[0] + all_code[len(chaifen)-1]
                    
                    if shoumo not in dict_data[character]:
                        dict_data[character].append(shoumo)
    return dict_data


# Function to update missing encodings in the file
def update_missing_encodings(file_path, write_file_path, dict_data):
    # Read the file content
    print(f"update_missing_encodings file_path: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    line_count = len(lines)
    processed_count = 0

    # 定义编码方案的固定顺序
    scheme_order = ['moqi', 'xh', 'zrm', 'jdh', 'cj', 'hm', 'wb', 'hx']

    # Process each line
    for line in lines:
        processed_count += 1
        if processed_count % 10000 == 0:
            print(f"Processed {processed_count}/{line_count} lines")
            
        line = line.rstrip('\n')
        if not line or line.startswith("#") or '\t' not in line:
            updated_lines.append(line)
            continue

        parts = line.split('\t')
        character = parts[0]
        encoding = parts[1]
        frequency = parts[2] if len(parts) > 2 else None

        if "tencent" in file_path:
            updated_line = f"{character}\t99"
            updated_lines.append(updated_line)
            continue
        else:
            if encoding == "100":
                updated_lines.append(line)
                continue

        pinyin_list = encoding.split(" ")
        double_list_parts = []
        pinyin_index = 0
        
        clean_character = character.replace("·", "")
        
        for pinyin in pinyin_list:
            double_pinyin = pinyin
            if pinyin_index >= len(clean_character):
                break
                
            character_encoding_pre = clean_character[pinyin_index]
            
            # 按照固定顺序处理所有编码方案，即使没有编码也要用空字符串占位
            encoding_post_parts = []
            for scheme in scheme_order:
                if scheme in dict_data and character_encoding_pre in dict_data[scheme]:
                    # 同一个编码方案的多个编码用逗号连接
                    scheme_codes = ','.join(dict_data[scheme][character_encoding_pre])
                    encoding_post_parts.append(scheme_codes)
                else:
                    # 没有编码的方案用空字符串占位
                    encoding_post_parts.append('')
            
            # 不同编码方案用分号分隔，最后加一个分号
            encoding_post_str = ';'.join(encoding_post_parts) + ';'
            double_list_parts.append(f"{double_pinyin};{encoding_post_str}")
            pinyin_index += 1
        
        double_list = ' '.join(double_list_parts)

        if "tencent" in file_path:
            updated_line = f"{character}\t99"
        else:
            if frequency is not None:
                updated_line = f"{character}\t{double_list}\t{frequency}"
            else:
                updated_line = f"{character}\t{double_list}"
        updated_lines.append(updated_line)

    # Write the updated content back to the file
    print(f"write_file_path: {write_file_path}")
    write_file(write_file_path, '\n'.join(updated_lines))

# Precompute dict_data
dict_data = {}
file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']

print("Loading dictionary data...")
dict_data['moqi'] = get_aux_code_map(['./opencc/moqi_chaifen.txt','./opencc/moqi_chaifen_rongcuo.txt'])
dict_data['xh'] = get_xh_aux_code_map(['./program/flypydz.yaml','./program/flypydz_g.yaml'])
dict_data['zrm'] = get_zrm_aux_code_map(['./program/moran.chars.dict.yaml'])
dict_data['jdh'] = get_aux_code_map(['./program/简单鹤有理版V6.0.3手心辅助码.txt'])
dict_data['cj'] = get_shoumo_aux_code_map(['./cangjie5.dict.yaml'])
dict_data['hm'] = get_hu_aux_code_map(['./program/hu_cf.txt'])
dict_data['wb'] = get_pre2_aux_code_map(['./program/wubi86.dict.yaml'])
dict_data['hx'] = get_shouxin_aux_code_map(['./program/汉心手心辅助码双码.txt'])

# Test prints
print("火字的编码测试:")
print("moqi:", dict_data['moqi']['火'])
print("xh:", dict_data['xh']['火'])
print("zrm:", dict_data['zrm']['火'])
print("hx:", dict_data['hx']['火'])

# Process main files
print("Processing main dictionary files...")
for file_name in file_list:
    cn_dicts_path = os.path.join(root_path, "cn_dicts")
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts', file_name)

    if os.path.exists(yaml_file_path):
        print(yaml_file_path)
        update_missing_encodings(yaml_file_path, write_file_path, dict_data)
    else:
        print(f"File not found: {yaml_file_path}")

# Process cell dictionary files
print("Processing cell dictionary files...")
cell_path = os.path.join(root_path, "cn_dicts_cell")
if os.path.exists(cell_path):
    for file_name in os.listdir(cell_path):
        yaml_file_path = os.path.join(cell_path, file_name)
        write_file_path = os.path.join('cn_dicts_cell', file_name)

        if os.path.isfile(yaml_file_path):
            print(yaml_file_path)
            update_missing_encodings(yaml_file_path, write_file_path, dict_data)
else:
    print(f"Cell path not found: {cell_path}")