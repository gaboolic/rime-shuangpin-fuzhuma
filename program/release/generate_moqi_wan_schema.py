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
folders = ['cn_dicts', 'cn_dicts_cell', 'cn_dicts_common','custom_phrase','lua','opencc']  
files = [
    'default.yaml', 'moqi_speller.yaml','moqi_wan.extended.dict.yaml',
         'moqi_wan_abc_mo.schema.yaml',
         'moqi_wan_flypy.schema.yaml',
         'moqi_wan_flypyhu.schema.yaml',
         'moqi_wan_flypymo.schema.yaml',
         'moqi_wan_jdh.schema.yaml',
         'moqi_wan_ms_wb.schema.yaml',
         'moqi_wan_quanpin_moqi.schema.yaml',
         'moqi_wan_sogou.schema.yaml',
         'moqi_wan_zrm_hx.schema.yaml',
         'moqi_wan_zrm.schema.yaml',

         'moqi_single_xh.schema.yaml','moqi_single.dict.yaml',

         'moqi_big.schema.yaml','moqi_big.extended.dict.yaml',
         'symbols_caps_v.yaml','rime.lua','moqi.yaml',
         
         'cangjie5.dict.yaml','cangjie5.schema.yaml','easy_en.dict.yaml','easy_en.schema.yaml',
         'emoji.dict.yaml','emoji.schema.yaml',
         'jp_sela.dict.yaml','jp_sela.schema.yaml',
         'radical_flypy.dict.yaml','radical_flypy.schema.yaml',
         'reverse_moqima.dict.yaml','reverse_moqima.schema.yaml',
         'zrlf.dict.yaml','zrlf.schema.yaml'
         ]  
zip_folders_and_files('rime-moqi-wanxiang-schemas.zip', folders, files)