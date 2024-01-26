const fs = require('fs');
const path = require('path');

// YAML文件的路径
const yamlFilePath = path.join(__dirname, '../flypy_flypy.dict.yaml');

// 异步读取YAML文件
fs.readFile(yamlFilePath, 'utf8', (err, data) => {
    if (err) {
        console.error('读取文件时发生错误:', err);
        return;
    }

    // 处理YAML内容
    parseYamlContent(data);
});

var one_list = `菜少僧多佛无肉 车新帅老将有云 深山谁能弄风月 水里咋让虐毛熊 黑龙森林闹天地 黄牛大户拨窗泥
阿翁恰好说空话 爱女当面色从容 怒撒红米她先笑 穷困绿囊贼也完 为何楼高汤更暖 凭啥桥坏应对难
目光绕得亲体软 装问跑来您眼前 两间长草各内外 几行热搜求安全 藏传真如修本主 上元太岁共双恩
桌边混吃仍需乐 村中走动且请跟 长路正顺或行久 报表群读谈分成 样图古怪撇粗乱 陈某特强蹦窜戳
配料过关调算法 嫩排开口要生抽 昂头每次旁若定 顿额经年只等盘 曾早数日听鸟梦 但因差点总卷然
四下帮凑含宁散 最后推却跌碰贴 超贵追买怕卡疼 放浪还看该干吗 亚奥比赛忙参与 想哭接连被灭团
费用加增够快否 普系吹落很亏么 占据民调都进组 受到肯夸找靠所 并列均宽纯末况 再而以测滚剖剋
破产另设做事处 挖坑则选横滨区 藏着换代别叫慢 错论白给任其催 刚送那些同学们 冲丢怎办转冷啦
品类套票盆克秒 名片副部段批扎 挂拽抗拴拖揣握 抓捏挪扫把扩擦 刘苏岑欧周王反 嗯欸喔哟嘎哈呢
得会拆字`

function parseYamlContent(yamlContent) {
    // 使用正则表达式匹配码表行
    const regex = /^(\S+)\s+(\S+)\[.*$/gm;
    let match;
    const codeTable = {};

    // 循环匹配所有符合条件的行
    while ((match = regex.exec(yamlContent)) !== null) {
        // 将匹配到的字和对应编码存储到codeTable对象中
        const character = match[1];
        const code = match[2];
        if (codeTable[character] == null)
            codeTable[character] = code;
    }

    // 输出码表
    // console.log(codeTable);



    for (var i = 0; i < one_list.length; i++) {
        var one = one_list[i]
        if (one == ' ' || one == '\n') {
            continue;
        }
        //todo 输出这个字的码表
        console.log(one + "\t" + codeTable[one] + "\t2")
    }
}
