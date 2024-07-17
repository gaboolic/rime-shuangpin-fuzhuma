import os

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
with open('./program/flypydz.yaml', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if "\t" in line:
            character, encoding = line.strip().split('\t')
            if "'" not in encoding:
                encoding_pre = encoding[:2]
                encoding_post = encoding[2:]
                # if character in '去我而人他有是出哦配啊算的非个和就可了在小从这吧你吗':
                #     if len(encoding_post) == 2:
                #         encoding_post = encoding_post[0] + encoding_post[1].upper()
                if character not in dict_data:
                    dict_data[character] = encoding_post


print("巴 " + dict_data['巴'])
print("𬱖 " + dict_data['𬱖'])

for file_name in file_list:
    # File paths
    cn_dicts_path = os.path.expanduser("~/vscode/rime-frost/cn_dicts")
    yaml_file_path = os.path.join(cn_dicts_path, file_name)
    write_file_path = os.path.join('cn_dicts_xh', file_name)

    print(yaml_file_path)
    # Update missing encodings in the file
    update_missing_encodings(yaml_file_path, write_file_path, dict_data)


yaml_file_path = os.path.join('cn_dicts_dazhu', 'cell.dict.yaml')
write_file_path = os.path.join('cn_dicts_xh', 'cell.dict.yaml')

print(yaml_file_path)
# Update missing encodings in the file
update_missing_encodings(yaml_file_path, write_file_path, dict_data)
