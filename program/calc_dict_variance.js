const fs = require('fs');
const path = require('path');

// dict文件的路径
// const dictFilePath = path.join(__dirname, '../flypydz.yaml');
// const dictFilePath = path.join(__dirname, '../xmjd6.danzi.dict.yaml');
// const dictFilePath = path.join(__dirname, '../moran.chars.dict.yaml');
const dictFilePath = path.join(__dirname, '../sbfd.dict.yaml');

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
        // const [character, encoding] = line.split('\t');
        const [character, a, b, encoding] = line.split('\t');
        if (encoding.indexOf("'") == -1) {
            var encoding_pre = encoding.substring(0, 2);

            if (dictData[encoding_pre] == null) {
                dictData[encoding_pre] = 1;
            } else {
                dictData[encoding_pre] += 1;
            }
            // else {
            //     if (dictData[character + encoding_pre] != encoding_post) {
            //         dictData[character + encoding_pre] = dictData[character + encoding_pre] + encoding_post;
            //         console.log("重复 " + character + encoding)
            //         repeat_count++
            //     }
            // }
        }
    }
});
console.log(dictData)
console.log(Object.keys(dictData).length);

// 计算数据的均值
const values = Object.values(dictData);
const mean = values.reduce((acc, curr) => acc + curr, 0) / values.length;
console.log("mean:" + mean)

// 计算平方差
const squaredDifferences = values.map(value => Math.pow(value - mean, 2));

// 计算方差
const variance = squaredDifferences.reduce((acc, curr) => acc + curr, 0) / (values.length - 1);

console.log("数据集的方差为: " + variance);