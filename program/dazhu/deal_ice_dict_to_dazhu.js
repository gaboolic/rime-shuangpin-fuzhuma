const fs = require('fs');
const path = require('path');


// 需要修改的YAML文件的路径
// 需要修改的YAML文件的路径
// const yamlFilePath = path.join(__dirname, '../cn_dicts_moqi/8105.dict.yaml');
const yamlFilePath = path.join(__dirname, '../moqi_single.dict.yaml');
// const yamlFilePath = path.join(__dirname, '../custom_phrase.txt');
// 需要修改的YAML文件的路径
const writeFilePath = path.join(__dirname, '../cn_dicts_dazhu/moqi_single.dict.txt');

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
function updateMissingEncodings(filePath, writeFilePath) {
    // Read the file content
    const fileContent = readFile(filePath);

    // Split the content into lines
    const lines = fileContent.split('\n');

    // Create an updated content variable
    let updatedContent = '';

    var encoding_count_map = {}
    // Process each line
    lines.forEach((line) => {
        // Assume each line has the format "字\t编码"
        if (!line.includes('\t') || line.startsWith("#")) {
            return
        }

        var [character, encoding, frequency] = line.split('\t');


        if (encoding == "100") {
            return
        }
        encoding = encoding.replace(/\[/g, "");
        pinyin_list = encoding.split(" ")
        new_encoding = ""
        for (pinyin of pinyin_list) {
            pinyin = pinyin.substring(0, 3)
            new_encoding += pinyin
        }
        //encoding = new_encoding


        if (encoding_count_map[encoding] == null) {
            encoding_count_map[encoding] = 1;
        } else {
            encoding_count_map[encoding] += 1;
        }

        // Update the line with the missing encoding
        var updatedLine = `${encoding}\t${character}`;

        if (encoding_count_map[encoding] < 7) {

            // Append the updated line to the updated content
            updatedContent += updatedLine + '\n';
        }

    });

    // Write the updated content back to the file
    writeFile(writeFilePath, updatedContent);
}


// Call the function to update missing encodings in the file
updateMissingEncodings(yamlFilePath, writeFilePath);