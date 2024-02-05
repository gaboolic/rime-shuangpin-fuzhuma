const fs = require('fs');
const path = require('path');

// dict文件的路径
const dictFilePath = path.join(__dirname, './flypydz.yaml');

// 同步读取YAML文件
const dictFileContent = fs.readFileSync(dictFilePath, 'utf8');

// 获取每个字的编码
//阿	aaek
// 按行分割文本数据
const dictLines = dictFileContent.split('\n');

// 解析每一行数据
const dictData = {};
dictLines.forEach((line) => {
    // 假设每行的格式为 "字\t编码"
    if (line.indexOf("\t") != -1) {
        const [character, encoding] = line.split('\t');
        if (encoding.indexOf("'") == -1) {
            var encoding_pre = encoding.substring(0, 2);
            var encoding_post = encoding.substring(2);
            dictData[character + encoding_pre] = encoding_post;
        }
    }
});

// 获取每个字的编码
console.log('编码:', dictData);

// YAML文件的路径
const yamlFilePath = path.join(__dirname, '../flypy_flypy.dict.yaml');

// 同步读取YAML文件
const yamlFileContent = fs.readFileSync(yamlFilePath, 'utf8');

// 按行分割文本数据
const yamlLines = yamlFileContent.split('\n');

// 需要获取编码的字
const needCodeDictData = {};
yamlLines.forEach((line) => {
    // 假设每行的格式为 "字\t编码"
    if (line.indexOf("\t") != -1) {
        const [character, encoding] = line.split('\t');

        var encoding_pre = encoding.substring(0, 2);
        var encoding_post = encoding.substring(3);

        if (encoding_post == '[') {
            needCodeDictData[character + encoding_pre] = encoding_post;
        }
    }
});

// 需要获取编码的字
console.log('编码:', needCodeDictData);




// 需要获取编码的字
const needUpdateDictData = {};
for (needCode in needCodeDictData) {
    dictCode = dictData[needCode];
    if (dictCode == null) {
        continue;
    }
    needUpdateDictData[needCode] = dictCode;
}
console.log(needUpdateDictData)




// Function to read a file
function readFile(filePath) {
    return fs.readFileSync(filePath, 'utf8');
}

// Function to write content to a file
function writeFile(filePath, content) {
    fs.writeFileSync(filePath, content, 'utf8');
}

// Function to update missing encodings in the file
function updateMissingEncodings(filePath) {
    // Read the file content
    const fileContent = readFile(filePath);

    // Split the content into lines
    const lines = fileContent.split('\n');

    // Create an updated content variable
    let updatedContent = '';

    // Process each line
    lines.forEach((line) => {
        // Assume each line has the format "字\t编码"
        if (line.includes('\t')) {
            const [character, encoding] = line.split('\t');

            var encoding_pre = encoding.substring(0, 2);
            var encoding_post = encoding.substring(3);

            if (encoding_post == '[') {
                needCodeDictData[character + encoding_pre] = encoding_post;
            }

            // Check if the encoding is missing
            if (encoding_post === '[' && needUpdateDictData[character + encoding_pre] != null) {
                // TODO: Add logic to generate and assign the missing encoding
                // For example, you can use a function to generate the encoding based on the character

                // Generate and assign the missing encoding
                const missingEncoding = needUpdateDictData[character + encoding_pre];

                // Update the line with the missing encoding
                const updatedLine = `${character}\t${encoding_pre}[${missingEncoding}`;

                // Append the updated line to the updated content
                updatedContent += updatedLine + '\n';
            } else {
                // The line already has an encoding, so append it as is
                updatedContent += line + '\n';
            }
        } else {
            // Append non-matching lines to the updated content
            updatedContent += line + '\n';
        }
    });

    // Write the updated content back to the file
    writeFile(filePath, updatedContent);
}


// Call the function to update missing encodings in the file
updateMissingEncodings(yamlFilePath);