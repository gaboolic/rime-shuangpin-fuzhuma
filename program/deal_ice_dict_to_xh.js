const fs = require('fs');
const path = require('path');

// dict文件的路径
const dictFilePath = path.join(__dirname, '../flypy_flypy.dict.yaml');

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
            var encoding_post = encoding.substring(3);
            dictData[character] = encoding_post;
        }
    }
});

// 获取每个字的编码
// console.log('编码:', dictData);
console.log("孙 " + dictData['孙'])

// 需要修改的YAML文件的路径
const yamlFilePath = path.join(__dirname, '../cn_dicts/base.dict.yaml');

// 同步读取YAML文件
const yamlFileContent = fs.readFileSync(yamlFilePath, 'utf8');

// 按行分割文本数据
const yamlLines = yamlFileContent.split('\n');


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
        if (line.includes('\t') && !line.startsWith("#")) {
            const [character, encoding, frequency] = line.split('\t');

            // console.log(encoding)

            pinyin_list = encoding.split(" ")
            double_list = ""
            var pinyin_index = 0
            for (pinyin of pinyin_list) {
                double_pinyin = ""
                if (pinyin.length == 2) {
                    double_pinyin = pinyin
                } else if (pinyin.length == 1) {
                    double_pinyin = pinyin + pinyin
                } else {
                    shengmu = pinyin.substring(0, 1)
                    yunmu = pinyin.substring(1)

                    double_shengmu = shengmu
                    if (pinyin.charAt(1) == "h") {
                        shengmu = pinyin.substring(0, 2)
                        yunmu = pinyin.substring(2)
                        shengmu_map = { "zh": "v", "ch": "i", "sh": "u" }
                        double_shengmu = shengmu_map[shengmu]
                    }
                    if (double_shengmu == 'a') {
                        yunmu = pinyin
                    }
                    if (double_shengmu == 'o') {
                        yunmu = pinyin
                    }
                    const yunmu_map = {
                        'iu': 'q',
                        'ei': 'w',
                        'uan': 'r',
                        'van': 'r',

                        'ue': 't',
                        've': 't',
                        'un': 'y',
                        'vn': 'y',
                        'uo': 'o',
                        'ie': 'p',

                        'iong': 's',
                        'ong': 's',

                        'ai': 'd',
                        'en': 'f',

                        'eng': 'g',
                        'ang': 'h',
                        'an': 'j',

                        'ing': 'k',
                        'uai': 'k',
                        'iang': 'l',
                        'uang': 'l',

                        'ou': 'z',
                        'ia': 'x',
                        'ua': 'x',
                        'ao': 'c',
                        'ui': 'v',
                        'in': 'b',

                        'iao': 'n',

                        'ian': 'm',
                    };
                    double_yummu = yunmu_map[yunmu]
                    if (yunmu.length == 1)
                        double_yummu = yunmu

                    double_pinyin = double_shengmu + double_yummu

                    if (double_pinyin.length != 2) {
                        console.log("!!!!double_pinyin " + double_pinyin + " " + pinyin + " ")
                    }
                }
                var clean_character = character.replace("·", "")
                var character_encoding_pre = clean_character.charAt(pinyin_index)
                encoding_post = dictData[character_encoding_pre];
                if (encoding_post == null) {
                    // console.log("!!!character_encoding_pre:" + character_encoding_pre)
                    // console.log("!!!!encoding_post==null " + double_pinyin + " " + pinyin + " character_encoding_pre:" + character_encoding_pre + " " + line)
                    // console.log("character:" + character)
                    // console.log("pinyin_index " + pinyin_index)
                    // console.log("pinyin " + pinyin)
                    // console.log("character.charAt(pinyin_index):" + character.charAt(pinyin_index))
                    // console.log("double_pinyin " + double_pinyin)
                }
                double_list += double_pinyin + "[" + encoding_post
                double_list += " "
                pinyin_index++
            }
            double_list = double_list.substring(0, double_list.length - 1)
            // Update the line with the missing encoding
            const updatedLine = `${character}\t${double_list}\t${frequency}`;
            console.log(updatedLine)
            // Append the updated line to the updated content
            updatedContent += updatedLine + '\n';
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