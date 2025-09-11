#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试易学码辅助码加载功能
"""
import os

# 获取当前文件所在目录的父目录（项目根目录）
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = root_path.replace('\\', '/')

# 定义获取手心辅助码格式的函数，与主程序中的get_shouxin_aux_code_map相同
def get_shouxin_aux_code_map(file_list):
    dict_data = {}
    for file in file_list:
        try:
            with open(file, 'r', encoding='utf-8') as dict_file:
                for line in dict_file:
                    if "=" not in line:
                        continue
                    params = line.strip().split('=')
                    character = params[0]
                    encoding = params[1]
                    if "'" not in encoding:
                        if character not in dict_data:
                            dict_data[character] = [encoding]
                        else:
                            if encoding not in dict_data[character]:
                                dict_data[character].append(encoding)
            print(f"成功加载文件: {file}")
        except Exception as e:
            print(f"加载文件失败 {file}: {e}")
    return dict_data

# 测试加载易学码文件
def test_yx_code():
    # 易学码文件路径
    yx_file_path = './program/手心辅易学码9.txt'
    
    # 确保文件存在
    if not os.path.exists(yx_file_path):
        print(f"错误: 找不到易学码文件 {yx_file_path}")
        print(f"当前工作目录: {os.getcwd()}")
        return
    
    # 加载易学码
    print("开始加载易学码...")
    yx_dict = get_shouxin_aux_code_map([yx_file_path])
    
    # 显示加载结果
    print(f"\n成功加载了 {len(yx_dict)} 个字符的易学码")
    
    # 测试一些常见字符
    test_chars = ['火', '水', '木', '金', '土', '中', '国', '人', '一', '你', '我', '他']
    print("\n测试字符的易学码:")
    for char in test_chars:
        if char in yx_dict:
            print(f"{char}: {yx_dict[char]}")
        else:
            print(f"{char}: 未找到易学码")
    
    # 检查字典结构是否正确
    print("\n字典结构验证:")
    sample_chars = list(yx_dict.keys())[:5] if len(yx_dict) >= 5 else list(yx_dict.keys())
    for char in sample_chars:
        codes = yx_dict[char]
        print(f"字符 '{char}' 的编码: {codes}, 类型: {type(codes)}")

if __name__ == "__main__":
    print("易学码辅助码测试工具")
    print("=" * 50)
    test_yx_code()
    print("=" * 50)
    print("测试完成")