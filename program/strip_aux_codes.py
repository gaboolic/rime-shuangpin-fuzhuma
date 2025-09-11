import os

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write content to a file
def write_file(file_path, content):
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to strip auxiliary codes from the dictionary file
def update_missing_encodings(file_path, write_file_path, dict_data=None):
    # Read the file content
    print(f"Processing file: {file_path}")
    file_content = read_file(file_path)

    # Split the content into lines
    lines = file_content.split('\n')

    # Create an updated content variable
    updated_content = ''

    print(f"Total lines: {len(lines)}")
    # Process each line
    for line in lines:
        # Skip comments and lines without tab separator
        if '\t' not in line or line.startswith("#"):
            updated_content += line + '\n'
            continue

        # Extract character, encoding and frequency (if exists)
        frequency = None
        if len(line.split('\t')) == 3:
            character, encoding, frequency = line.split('\t')
        else:
            character, encoding = line.split('\t')

        # Skip tencent special handling (if needed)
        if "tencent" in file_path:
            updated_line = f"{character}\t99"
            updated_content += updated_line + '\n'
            continue
        else:
            if encoding == "100":
                updated_content += line + '\n'
                continue

        # Process encoding: extract pinyin parts before semicolons
        pinyin_list = encoding.split(" ")
        clean_pinyins = []
        
        for pinyin_part in pinyin_list:
            # Split on semicolon and take the first part (pure pinyin)
            if ';' in pinyin_part:
                clean_pinyin = pinyin_part.split(';')[0]
                clean_pinyins.append(clean_pinyin)
            else:
                # If no semicolon, keep as is
                clean_pinyins.append(pinyin_part)
        
        # Join the clean pinyins
        clean_encoding = " ".join(clean_pinyins)
        
        # Create the updated line with or without frequency
        if frequency is not None:
            updated_line = f"{character}\t{clean_encoding}\t{frequency}"
        else:
            updated_line = f"{character}\t{clean_encoding}"
        
        updated_content += updated_line + '\n'

    # Write the updated content back to the file
    print(f"Writing to: {write_file_path}")
    write_file(write_file_path, updated_content)
    print("Processing completed.")

# Example usage if this script is run directly
if __name__ == "__main__":
    # 获取当前文件所在目录的父目录（项目根目录）
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 示例：处理8105.dict.yaml文件
    file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
    for file_name in file_list:
        # File paths
        cn_dicts_path = os.path.join(root_path, "cn_dicts")
        yaml_file_path = os.path.join(cn_dicts_path, file_name)
        write_file_path = os.path.join('cn_dicts', file_name)

        print(yaml_file_path)
        # Update missing encodings in the file
        update_missing_encodings(yaml_file_path, write_file_path, None)