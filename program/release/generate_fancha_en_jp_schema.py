import zipfile  
import os  
  
def zip_folders_and_files(zip_name, folders, files):  
    """  
    将指定的多个文件夹和文件打包成一个ZIP文件。  
  
    :param zip_name: 输出的ZIP文件名  
    :param folders: 要打包的文件夹名列表  
    :param files: 要打包的文件名列表  
    """  
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:  
        # 添加文件夹  
        for folder in folders:  
            for root, dirs, files_in_folder in os.walk(folder):  
                for file in files_in_folder:  
                    file_path = os.path.join(root, file)  
                    arcname = os.path.relpath(file_path, os.path.dirname(folder))  
                    zipf.write(file_path, arcname)  
          
        # 添加文件  
        for file in files:  
            if os.path.isfile(file):  
                zipf.write(file, os.path.basename(file))  
  
# 使用示例  
folders = []  
files = ['cangjie5.dict.yaml','cangjie5.schema.yaml','easy_en.dict.yaml','easy_en.schema.yaml',
         'emoji.dict.yaml','emoji.schema.yaml',
         'jp_sela.dict.yaml','jp_sela.schema.yaml',
         'radical_flypy.dict.yaml','radical_flypy.schema.yaml',
         'reverse_moqima.dict.yaml','reverse_moqima.schema.yaml',
         'zrlf.dict.yaml','zrlf.schema.yaml'
         ]  
zip_folders_and_files('rime-reverse-and-english-and-emoji.zip', folders, files)