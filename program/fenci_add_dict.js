//https://github.com/luckykaiyi/nodejieba
//npm install nodejieba

// 使用 require 导入 nodejieba 模块
const nodejieba = require("nodejieba");

// 进行中文分词
// const text = "不是善茬";
var text = "输入短语的时候"
var text = "鱼的"
nodejieba.insertWord("一万")
const result = nodejieba.cutAll(text);

// 输出分词结果
console.log(result);



const fs = require('fs');
const path = require('path');

function get_word_set(filePath) {

    // dict文件的路径
    const dictFilePath = filePath;

    // 同步读取YAML文件
    const dictFileContent = fs.readFileSync(dictFilePath, 'utf8');

    // 获取每个字的编码
    //阿	aaek
    // 按行分割文本数据
    const dictLines = dictFileContent.split('\n');

    const word_set = new Set();
    repeat_count = 0
    // 解析每一行数据
    const dictData = {};
    dictLines.forEach((line) => {
        // 假设每行的格式为 "字\t编码"
        if (line.indexOf("\t") != -1) {
            const [character, encoding] = line.split('\t');
            word_set.add(character)

        }
    });
    return word_set;
}
const dict_word_count = {}
function get_word_fenci_set() {

    // dict文件的路径
    const dictFilePath = path.join(__dirname, './三体1疯狂年代.txt');

    // 同步读取YAML文件
    const dictFileContent = fs.readFileSync(dictFilePath, 'utf8');

    // 获取每个字的编码
    //阿	aaek
    // 按行分割文本数据
    const dictLines = dictFileContent.split('\n');

    const fenci_set = new Set();
    repeat_count = 0
    // 解析每一行数据
    const dictData = {};
    dictLines.forEach((line) => {
        // 假设每行的格式为 "字\t编码"
        const result = nodejieba.cut(line);

        if (result.length > 1) {
            // 将分词结果添加到 Set 中
            result.forEach(word => {

                if (word.length > 1) {
                    fenci_set.add(word);
                }

                if (dict_word_count[word] == undefined) {
                    dict_word_count[word] = 1;
                } else {
                    dict_word_count[word] += 1;
                }

            });
        }
    });
    return fenci_set;
}
const file_list = ['base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
const dict_word_set = new Set();

for (file_name of file_list) {
    const yamlFilePath = path.join(__dirname, '../cn_dicts/', file_name);

    const word_set = get_word_set(yamlFilePath)
    // 将每个文件的单词集合合并到 dict_word_set 中
    word_set.forEach(word => {
        dict_word_set.add(word);



    });
}
console.log(dict_word_set.size)

dict_word_set.forEach(word => {
    nodejieba.insertWord(word);
});



const tencent_file_list = ['tencent.dict.yaml']
for (file_name of tencent_file_list) {
    const yamlFilePath = path.join(__dirname, '../cn_dicts/', file_name);

    const word_set = get_word_set(yamlFilePath)
    // 将每个文件的单词集合合并到 dict_word_set 中
    word_set.forEach(word => {
        dict_word_set.add(word);
    });
}


const fenci_word_set = get_word_fenci_set()

console.log(fenci_word_set.size)
console.log(fenci_word_set)

console.log(dict_word_count)

// 将对象转换为可排序的数组
const sortedEntries = Object.entries(dict_word_count).sort((a, b) => a[1] - b[1]);

// 输出排序后的结果
// 准备要写入文件的文本内容
let outputData = '';
sortedEntries.forEach(entry => {
    console.log(`${entry[0]}: ${entry[1]}`);
    outputData += `${entry[0]}: ${entry[1]}\n`;
});

// 输出在 fenci_word_set 中但不在 dict_word_set 中的词汇
const words_not_in_dict = new Set();
fenci_word_set.forEach(word => {
    if (!dict_word_set.has(word) && word.length <= 3) {
        words_not_in_dict.add(word);
    }
});

console.log(words_not_in_dict.size)

// // 打印结果
// words_not_in_dict.forEach(word => {
//     console.log(word);
// });
// 将不在 dict_word_set 中且长度小于等于 3 的词汇写入文件
fs.writeFileSync('words_not_in_dict.txt', Array.from(words_not_in_dict).join('\n'));

// 将排序后的结果写入文件
fs.writeFile('fenci_2ci.txt', outputData, 'utf8', (err) => {
    if (err) {
        console.error('写入文件时发生错误：', err);
        return;
    }
    console.log('排序后的结果已成功写入文件！');
});