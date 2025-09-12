import os
import sys

# 获取当前文件所在目录的父目录（项目根目录）
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 确保路径在Windows环境下正确表示
root_path = root_path.replace('\\', '/')

# 确保项目根目录在Python路径中
sys.path.append(root_path)

"""
统一的文件路径处理逻辑
返回需要处理的文件列表和它们的路径信息
"""
def get_file_paths():
    file_info = []
    
    # 处理主要词库文件
    file_list = ['8105.dict.yaml', '41448.dict.yaml', 'base.dict.yaml', 'ext.dict.yaml', 'others.dict.yaml']
    for file_name in file_list:
        # 文件路径
        cn_dicts_path = os.path.join(root_path, "cn_dicts")
        yaml_file_path = os.path.join(cn_dicts_path, file_name)
        write_file_path = os.path.join('cn_dicts', file_name)
        
        file_info.append({
            'file_name': file_name,
            'source_path': yaml_file_path,
            'target_path': write_file_path
        })
    
    # 处理细胞词库文件
    cell_path = os.path.join(root_path, "cn_dicts_cell")
    if os.path.exists(cell_path):
        for file_name in os.listdir(cell_path):
            # 文件路径
            yaml_file_path = os.path.join(cell_path, file_name)
            write_file_path = os.path.join('cn_dicts_cell', file_name)
            
            file_info.append({
                'file_name': file_name,
                'source_path': yaml_file_path,
                'target_path': write_file_path
            })
    
    return file_info

"""
执行strip_aux_codes.py脚本
"""
def run_strip_aux_codes():
    print("===== 开始执行strip_aux_codes.py =====")
    
    # 直接调用原始脚本，避免重复执行
    import subprocess
    import sys
    
    # 构建strip_aux_codes.py的完整路径
    strip_script_path = os.path.join(root_path, "program", "strip_aux_codes.py")
    
    # 使用subprocess执行脚本，避免模块导入时的副作用
    print(f"执行脚本: {strip_script_path}")
    subprocess.run([sys.executable, strip_script_path], check=True, cwd=root_path)
    
    print("===== strip_aux_codes.py执行完成 =====")

"""
执行deal_ice_dict_to_moqi_wan.py脚本
"""
def run_deal_ice_dict_to_moqi_wan():
    print("===== 开始执行deal_ice_dict_to_moqi_wan.py =====")
    
    # 直接调用原始脚本，避免重复执行
    import subprocess
    import sys
    
    # 构建deal_ice_dict_to_moqi_wan.py的完整路径
    deal_script_path = os.path.join(root_path, "program", "deal_ice_dict_to_moqi_wan.py")
    
    # 使用subprocess执行脚本，避免模块导入时的副作用
    print(f"执行脚本: {deal_script_path}")
    subprocess.run([sys.executable, deal_script_path], check=True, cwd=root_path)
    
    print("===== deal_ice_dict_to_moqi_wan.py执行完成 =====")

"""
主函数
"""
def main():
    # 1. 首先执行strip_aux_codes.py，只保留拼音
    run_strip_aux_codes()
    
    # 2. 然后执行deal_ice_dict_to_moqi_wan.py，添加映射关系
    run_deal_ice_dict_to_moqi_wan()
    
    print("所有处理完成！")

if __name__ == "__main__":
    main()