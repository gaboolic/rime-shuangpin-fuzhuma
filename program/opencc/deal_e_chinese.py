write_file = open('cn_dicts_dazhu/english_chinese.txt', 'w')

word_list = []
with open('opencc/english_chinese.txt', 'r', encoding='utf-8') as dict_file:
    # 一下	一下 once / all of a sudden
    for line in dict_file:
        if not '\t' in line or line.startswith("#"):
            continue
        line = line.strip()
        params = line.split('\t')

        english = params[0]
        chinese = params[1]
        chinese = chinese.replace(" ","")
        chinese = chinese.replace("@"," ")

        for word in english.split("|"):
            if word == '':
                continue
            if word in word_list:
                print("!!!!!"+word)
                print(line)
            else :
                word_list.append(word)
            new_line = word + "\t" + word +" "
            new_line += chinese
            write_file.write(new_line+"\n")


        