const fs = require('fs');

// 文件路径数组
const filepaths = ['file1.txt', 'file2.txt', 'file3.txt'];

// 用于保存最终的拼接内容
let concatenatedContent = '';

// 读取每个文件的内容并拼接起来
filepaths.forEach(filepath => {
    let content = fs.readFileSync(filepath, 'utf8');
    concatenatedContent += content;
});

// 将拼接后的内容写入新文件
fs.writeFileSync('output.txt', concatenatedContent, 'utf8');

console.log('Files have been concatenated successfully!');
