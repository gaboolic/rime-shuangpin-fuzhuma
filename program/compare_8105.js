const fs = require('fs');
const path = require('path');



// dict文件的路径
// const dictFilePath = path.join(__dirname, '../cn_dicts_xh/', '8105.dict.yaml'); //802
// const dictFilePath = path.join(__dirname, '../cn_dicts_moqi/', '8105.dict.yaml'); //792
// const dictFilePath = path.join(__dirname, '../cn_dicts_xh/', '8105.dict.yaml'); //686
const dictFilePath = path.join(__dirname, '../cn_dicts_zrm/', '8105.dict.yaml'); //1487

// 同步读取YAML文件
const dictFileContent = fs.readFileSync(dictFilePath, 'utf8');

// 获取每个字的编码
//阿	aaek
// 按行分割文本数据
const dictLines = dictFileContent.split('\n');

repeat_count = 0
// 解析每一行数据
const dictData = {};
dictLines.forEach((line) => {
    // 假设每行的格式为 "字\t编码"
    if (line.indexOf("\t") != -1) {
        const [character, encoding] = line.split('\t');
        if (encoding.indexOf("'") == -1) {

            if (dictData[encoding] == null) {
                dictData[encoding] = character;
            }
            else {
                if (dictData[encoding] != character) {
                    dictData[encoding] = dictData[encoding] + character;
                    console.log("重复 " + encoding + dictData[encoding])
                    repeat_count++
                }
            }
        }
    }
});

console.log(Object.keys(dictData).length);

// 获取每个字的编码
// console.log('编码:', dictData);
console.log("巴 " + dictData['巴'])
console.log("日 " + dictData['日'])
console.log(repeat_count)



