write_file = open('cn_dicts_dazhu/english_chinese.txt', 'w')

with open('opencc/english_chinese.txt', 'r', encoding='utf-8') as dict_file:
    # 一下	一下 once / all of a sudden
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')

        english = params[0]
        chinese = params[1]
        # print(chinese)
        # if '\\n' in chinese:
        #     n_index =  chinese.index('\\n')
        #     pre_word = chinese[0:n_index]
        #     print(pre_word)
        #     if pre_word == english:
        #         print("====")
        #     chinese = chinese[n_index+2:]
        #     #print(chinese)

        new_line = english + "\t" + english +" "
        new_line += chinese.replace("\\n"," ")
        write_file.write(new_line+"\n")