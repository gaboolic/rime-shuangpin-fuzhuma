line_list = []
with open('./opencc/moqi_chaifen.txt', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if "\t" in line:
            character, encoding, chaifen = line.strip().split('\t')
            line = f"{character}={encoding}"
            line_list.append(line)

write_file_name = "shouxin-moqi-aux-code-for-shouxin-input-method.txt"
write_file = open(write_file_name, 'w')

for line in line_list:
    write_file.write(line)
    write_file.write("\n")