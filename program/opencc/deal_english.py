write_file = open('cn_dicts_dazhu/chinese_english.txt', 'w')

with open('opencc/chinese_english.txt', 'r', encoding='utf-8') as dict_file:
    # 一下	一下 once / all of a sudden
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')

        chinese = params[0]
        english = params[1][len(chinese)+1:]
        new_line = chinese + "\t" + chinese +" "
        englishs = english.split(" / ")
        for word in englishs:
            word = word.replace(" "," ")
            new_line += word
            new_line += " "
        new_line = new_line[0:-1]
        write_file.write(new_line+"\n")