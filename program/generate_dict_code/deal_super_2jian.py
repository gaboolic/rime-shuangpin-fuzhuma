import os
import string
default_str = """
上午	uw/
数字	uz/
注册	vc/
知道	vd/
正常	vi/
知识	vu/
这样	vy/
正在	vz/
为此	wc/
网络	wl/
温暖	wn/
玩偶	wo/
万人	wr/
完善	wu/
位于	wy/
小儿	xe/
消费	xf/
相关	xg/
辛苦	xk/
下面	xm/
心情	xq/
显示	xu/
一定	yd/
因而	ye/
以及	yj/
游客	yk/
以来	yl/
页面	ym/
一年	yn/
意思	ys/
一下	yx/
由于	yy/
样子	yz/
自动	zd/
最快	zk/
子女	zn/
总算	zs/
赞同	zt/
文字	wz/
水平	up/
少年	un/
时候	uh/
收购	ug/
收到	ud/
收藏	uc/
探讨	tt/
提升	tu/
软盘	rp/
热情	rq/
妻子	qz/
欺诈	qv/
千万	qw/
清楚	qi/
批准	pv/
怄气	oq/
宁愿	ny/
妹妹	mm/
面积	mj/
领取	lq/
理念	ln/
良好	lh/
渴望	kw/
记者	jv/
继续	jx/
创造	iz/
出来	il/
很快	hk/
共同	gt/
公开	gk/
公安	ga/
否认	fr/
发帖	ft/
当初	di/
盎司	as/
爱心	ax/
牛逼	nb/
版本	bb/
怎样	zy/
老是	lu/
肯定	kd/
同意	ty/
渐渐	jj/
"""
default_map = {}
for line in default_str.split("\n"):
    if line == '':
        continue
    params = line.split("\t")
    word = params[0]
    encode = params[1][0:-1]
    default_map[encode] = word

jianpin_word_map = {}
file_list = ['base.dict.yaml','ext.dict.yaml']
for file in file_list:
    file_name = os.path.join('cn_dicts_moqi', file)
    with open(file_name, 'r') as file:
        # 逐行读取文件内容
        for line in file:
            # 去除行尾的换行符
            line = line.rstrip()
            if line.startswith('#') or '\t' not in line:
                continue
            params = line.split("\t")
            word = params[0]
            freq = params[2]
            
            if len(word) != 2:
                continue
            pinyin = params[1]
            shengmus = pinyin.split(" ")
            jianpin = shengmus[0][0] + shengmus[1][0]

            word_freq = {}
            word_freq["word"] = word
            word_freq["freq"] = freq
            if jianpin not in jianpin_word_map:
                word_list = []
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list
            else:
                word_list = jianpin_word_map[jianpin]
                word_list.append(word_freq)
                jianpin_word_map[jianpin] = word_list

# print(jianpin_word_map)


# 生成 'aa' 到 'az' 的字符串序列
letters = string.ascii_lowercase
combinations = [a + b for a in letters for b in letters]

file_path = "custom_phrase/custom_phrase_super_2jian.txt"
with open(file_path, "w") as file:
    file.write("## 超强2简 26*26=676词空间。 使用deal_super_2jian.py生成\n")
# 遍历字符串序列
    for combination in combinations:
        if combination not in jianpin_word_map:
            # print(combination)
            pass
        else:
            word_freq_list = jianpin_word_map[combination]
            # 对字典列表进行排序
            word_freq_list = sorted(word_freq_list, key=lambda x: int(x['freq']), reverse=True)

            # 取出前三个元素
            word_freq_list = word_freq_list[:3]
            word = word_freq_list[0]['word']
            if word == '但是':
                word = '都是'
            if word == '现在':
                word = '选择'
            if word == '所以':
                word = '所有'
            if word == '认为':
                word = '让我'
            if word == '自己':
                word = '最近'
            if word == '目前':
                word = '明确'
            if word == '只是':
                word = '知识'
            if word == '不再':
                word = '不在'
            if word == '受到':
                word = '收到'
            if word == '感觉':
                word = '国家'
            if word == '过去':
                word = '感情'
            if word == '认真':
                word = '日志'
            if word == '申请':
                word = '失去'
            if word == '准备':
                word = '这边'
            if word == '比如':
                word = '别人'
            
            if combination in default_map:
                word = default_map[combination]
                print(word)
            if combination == 'al':
                word = '阿里'
            if combination == 'bq':
                word = '抱歉'
            if combination == 'cc':
                word = '从此'
            if combination == 'cd':
                word = '菜单'
            if combination == 'dh':
                word = '电话'
            if combination == 'dq':
                word = '地区'
            if combination == 'dr':
                word = '当然'
            if combination == 'ds':
                word = '打算'
            if combination == 'dv':
                word = '地址'
            if combination == 'dw':
                word = '单位'
            if combination == 'en':
                word = '二年'
            if combination == 'ff':
                word = '纷纷'
            if combination == 'fs':
                word = '发送'
            if combination == 'fy':
                word = '反应'
            if combination == 'gc':
                word = '刚才'
            if combination == 'gn':
                word = '国内'
            if combination == 'hb':
                word = '回报'
            if combination == 'hg':
                word = '韩国'
            if combination == 'hh':
                word = '呵呵'
            if combination == 'jq':
                word = '机器'
            if combination == 'hr':
                word = '忽然'
            if combination == 'ih':
                word = '场合'
            if combination == 'yi':
                word = '异常'
            if combination == 'jd':
                word = '记得'
            if combination == 'jg':
                word = '几个'
            if combination == 'jn':
                word = '今年'
            if combination == 'kl':
                word = '快乐'
            if combination == 'kg':
                word = '开关'
            if combination == 'kt':
                word = '空调'
            if combination == 'ld':
                word = '来到'
            if combination == 'ud':
                word = '受到'
            if combination == 'lj':
                word = '了解'
            if combination == 'ml':
                word = '美丽'
            if combination == 'mh':
                word = '美好'
            if combination == 'nh':
                word = '女孩'
            if combination == 'nn':
                word = '牛奶'
            if combination == 'nw':
                word = '内外'
            if combination == 'nz':
                word = '女子'
            if combination == 'pl':
                word = '疲劳'
            if combination == 'rh':
                word = '如何'
            if combination == 'rf':
                word = '若非'
            if combination == 'rm':
                word = '人民'
            if combination == 'rd':
                word = '认定'
            if combination == 'rt':
                word = '人体'
            if combination == 'tv':
                word = '调整'
            if combination == 'tx':
                word = '体系'
            if combination == 'ul':
                word = '数量'
            if combination == 'uu':
                word = '事实'
            if combination == 'vr':
                word = '主任'
            if combination == 'vw':
                word = '职位'
            if combination == 'xl':
                word = '心理'
            if combination == 'yp':
                word = '一篇'
            if combination == 'um':
                word = '上面'
            if combination == 'fz':
                word = '否则'
            if combination == 'qu':
                word = '确实'
            if combination == 'eq':
                word = '二区'
            if combination == 'pu':
                word = '评审'
            if combination == 'xd':
                word = '许多'
            if combination == 'nm':
                word = '你们'
            if combination == 'my':
                word = '满意'
            if combination == 'yb':
                word = '一遍'
            if combination == 'yv':
                word = '一种'
            if combination == 'zm':
                word = '咱们'
            if combination == 'fx':
                word = '分享'
            if combination == 'av':
                word = '安装'
            if combination == 'vm':
                word = '专门'
            if combination == 'gg':
                word = '哥哥'
            if combination == 'vn':
                word = '智能'
            if combination == 'bl':
                word = '遍历'
            if combination == 'ww':
                word = '往往'
            if combination == 'xz':
                word = '下载'
            if combination == 'ng':
                word = '哪个'
            if combination == 'cv':
                word = '从中'
            if combination == 'dx':
                word = '对象'
            if combination == 'vq':
                word = '追求'
            file.write(word+"\t"+combination+"/\n")
            # print(combination + " " + str(word_freq_list))
        # print(combination + jianpin_word_map[combination])