#!/usr/bin/env python3
"""同步上游词库（rime-frost），并为每个字追加墨奇码等辅助码。

用法：
    python program/deal_ice_dict_to_moqi_wan.py --upstream-dir /path/to/rime-frost

--upstream-dir 指向 rime-frost 仓库根目录（需要包含 cn_dicts/ 与 cn_dicts_cell/），
生成结果写回本仓库的 cn_dicts/ 与 cn_dicts_cell/。

说明：
- 上游的词条、注释、文件头会原样保留，只在每个拼音后追加辅助码。
- 本地独有的词条会被保留，避免定时同步时误删手工补充的内容。
"""

import argparse
import os
import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 需要同步的字词库
MAIN_DICT_FILES = [
    '8105.dict.yaml',
    '41448.dict.yaml',
    'GB18030-2022.dict.yaml',
    'base.dict.yaml',
    'ext.dict.yaml',
    'others.dict.yaml',
]

# 追加辅助码时各编码方案的固定顺序
SCHEME_ORDER = ['moqi', 'xh', 'zrm', 'jdh', 'cj', 'hm', 'wb', 'hx']


# Function to write content to a file
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        print(file_path)
        file.write(content)


def parse_entry(line):
    """把一行词库拆成 (词条, 编码, 词频)。

    上游偶尔会把「词条 拼音」写在同一列，例如 `米提亚 mi ti ya\\t15`，
    这里做一次兼容修正，避免生成错误的编码。
    """
    parts = line.split('\t')
    character = parts[0]
    encoding = parts[1] if len(parts) > 1 else None
    frequency = parts[2] if len(parts) > 2 else None

    if len(parts) == 2 and encoding is not None and ' ' in character:
        try:
            float(encoding)
        except ValueError:
            pass
        else:
            # 第二列其实是词频，第一列里才是「词条 拼音」
            if frequency is None:
                frequency = encoding
            tokens = character.split()
            character = tokens[0]
            encoding = ' '.join(tokens[1:])

    return character, encoding, frequency


# 没有制表符、但形如「词条 pin yin [词频]」的异常行
_UNTABBED_ENTRY_RE = re.compile(
    r'^(\S+)\s+([a-z]+(?:\s+[a-z]+)*)(?:\s+(\d+(?:\.\d+)?))?$')


def normalize_untabbed_entry(line):
    """把缺少制表符的异常词条行修正为 `词条\\t拼音[\\t词频]`。

    只处理「中文词条 + 纯小写拼音」这种非常明确的形式，其余行返回 None。
    """
    match = _UNTABBED_ENTRY_RE.match(line.strip())
    if not match:
        return None

    character, pinyin, frequency = match.groups()
    if character.isascii():
        return None

    if frequency is None:
        return f"{character}\t{pinyin}"
    return f"{character}\t{pinyin}\t{frequency}"


def get_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    if encoding not in dict_data[character]:
                        dict_data[character].append(encoding)
    return dict_data


def get_shouxin_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "=" not in line:
                    continue
                params = line.strip().split('=')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    if encoding not in dict_data[character]:
                        dict_data[character].append(encoding)
    return dict_data


def get_xh_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                line = line.strip()
                if not line or "\t" not in line:
                    continue

                params = line.split('\t')
                if len(params) < 2:
                    continue

                first = params[0]
                second = params[1]

                if len(first) == 1 and not first.isascii():
                    character = first
                    encoding = second
                else:
                    character = second
                    encoding = first

                if "'" in encoding:
                    continue

                if encoding.startswith('!') or encoding.startswith('/'):
                    continue

                for raw_code in encoding.split(','):
                    code_part = raw_code.strip()
                    if not code_part or "'" in code_part:
                        continue
                    if code_part.startswith('!') or code_part.startswith('/'):
                        continue

                    encoding_post = code_part[-2:]
                    if encoding_post not in dict_data[character]:
                        dict_data[character].append(encoding_post)
    return dict_data


def get_yehe_aux_code_map(file_list):
    dict_data = defaultdict(list)

    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                line = line.strip()
                if not line or "\t" not in line:
                    continue

                params = line.split('\t')
                if len(params) < 2:
                    continue

                first = params[0]
                second = params[1]

                if len(first) == 1 and not first.isascii():
                    character = first
                    encoding = second
                else:
                    character = second
                    encoding = first

                if "'" in encoding:
                    continue

                if encoding.startswith('!') or encoding.startswith('/'):
                    continue

                for raw_code in encoding.split(','):
                    code_part = raw_code.strip()
                    if not code_part or "'" in code_part:
                        continue
                    if code_part.startswith('!') or code_part.startswith('/'):
                        continue

                    encoding_post = code_part[-2:]
                    if encoding_post not in dict_data[character]:
                        dict_data[character].append(encoding_post)

    return dict_data


def get_zrm_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    if ";" not in encoding:
                        continue
                    encoding_post = encoding.split(";", 1)[1]
                    if encoding_post not in dict_data[character]:
                        dict_data[character].append(encoding_post)
    return dict_data


def get_shoumo_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                params = line.split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    shoumo_encode = encoding[0] + encoding[-1]
                    if shoumo_encode not in dict_data[character]:
                        dict_data[character].append(shoumo_encode)
    return dict_data


def get_pre2_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if "'" not in encoding:
                    encoding_pre = encoding[:2]
                    if encoding_pre not in dict_data[character]:
                        dict_data[character].append(encoding_pre)
    return dict_data


def get_hu_aux_code_map(file_list):
    dict_data = defaultdict(list)
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as dict_file:
            for line in dict_file:
                if "\t" not in line:
                    continue
                params = line.strip().split('\t')
                if len(params) < 2:
                    continue
                character = params[0]
                encoding = params[1]
                if encoding.startswith('〔') and encoding.endswith('〕'):
                    encoding = encoding[1:-1]
                    encodeings = encoding.split("&nbsp;·&nbsp;")
                    if len(encodeings) < 2:
                        continue
                    chaifen = encodeings[0]
                    all_code = encodeings[1]

                    if len(chaifen) == 1:
                        shoumo = all_code[0] + all_code[-1]
                    else:
                        shoumo = all_code[0] + all_code[len(chaifen)-1]

                    if shoumo not in dict_data[character]:
                        dict_data[character].append(shoumo)
    return dict_data


def build_dict_data():
    def repo_file(*parts):
        return str(REPO_ROOT.joinpath(*parts))

    print("Loading dictionary data...")
    dict_data = {}
    dict_data['moqi'] = get_aux_code_map([
        repo_file('opencc', 'moqi_chaifen.txt'),
        repo_file('opencc', 'moqi_chaifen_rongcuo.txt'),
    ])
    dict_data['xh'] = get_yehe_aux_code_map([
        repo_file('program', 'flypydz.yaml'),
        repo_file('program', 'flypydz_g.yaml'),
        repo_file('program', '野鹤.txt'),
    ])
    dict_data['zrm'] = get_zrm_aux_code_map([
        repo_file('program', 'moran.chars.dict.yaml'),
    ])
    dict_data['jdh'] = get_aux_code_map([
        repo_file('program', '简单鹤V9.2.0手心辅助码.txt'),
    ])
    dict_data['cj'] = get_shoumo_aux_code_map([
        repo_file('cangjie5.dict.yaml'),
    ])
    dict_data['hm'] = get_hu_aux_code_map([
        repo_file('program', 'hu_cf.txt'),
    ])
    dict_data['wb'] = get_pre2_aux_code_map([
        repo_file('program', 'wubi86.dict.yaml'),
    ])
    dict_data['hx'] = get_shouxin_aux_code_map([
        repo_file('program', '汉心手心辅助码双码.txt'),
    ])
    return dict_data


def build_updated_content(file_path, dict_data):
    """读取上游词库，为每个音节追加辅助码，返回生成的内容。"""
    print(f"update_missing_encodings file_path: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    line_count = len(lines)
    processed_count = 0

    for line in lines:
        processed_count += 1
        if processed_count % 10000 == 0:
            print(f"Processed {processed_count}/{line_count} lines")

        line = line.rstrip('\n')
        if not line or line.startswith("#"):
            updated_lines.append(line)
            continue

        if '\t' not in line:
            normalized = normalize_untabbed_entry(line)
            if normalized is None:
                updated_lines.append(line)
                continue
            line = normalized

        character, encoding, frequency = parse_entry(line)
        if not character or encoding is None:
            updated_lines.append(line)
            continue

        if "tencent" in str(file_path):
            updated_lines.append(f"{character}\t99")
            continue
        else:
            if encoding == "100":
                updated_lines.append(line)
                continue

        pinyin_list = encoding.split(" ")
        double_list_parts = []
        pinyin_index = 0

        clean_character = character.replace("·", "")

        for pinyin in pinyin_list:
            double_pinyin = pinyin
            if pinyin_index >= len(clean_character):
                break

            character_encoding_pre = clean_character[pinyin_index]

            # 按照固定顺序处理所有编码方案，即使没有编码也要用空字符串占位
            encoding_post_parts = []
            for scheme in SCHEME_ORDER:
                if scheme in dict_data and character_encoding_pre in dict_data[scheme]:
                    # 同一个编码方案的多个编码用逗号连接
                    scheme_codes = ','.join(dict_data[scheme][character_encoding_pre])
                    encoding_post_parts.append(scheme_codes)
                else:
                    # 没有编码的方案用空字符串占位
                    encoding_post_parts.append('')

            # 不同编码方案用分号分隔，最后加一个分号
            encoding_post_str = ';'.join(encoding_post_parts) + ';'
            double_list_parts.append(f"{double_pinyin};{encoding_post_str}")
            pinyin_index += 1

        double_list = ' '.join(double_list_parts)

        if frequency is not None:
            updated_line = f"{character}\t{double_list}\t{frequency}"
        else:
            updated_line = f"{character}\t{double_list}"
        updated_lines.append(updated_line)

    return '\n'.join(updated_lines)


def keep_local_only_entries(content, local_file):
    """保留本地独有、上游没有的词条，避免定时同步删除手工补充内容。"""
    if not os.path.exists(local_file):
        return content

    generated_words = {
        line.split('\t')[0]
        for line in content.split('\n')
        if '\t' in line and not line.startswith('#')
    }

    extra_lines = []
    with open(local_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.rstrip('\n')
            if not line or line.startswith('#') or '\t' not in line:
                continue
            if line.split('\t')[0] not in generated_words:
                extra_lines.append(line)

    if not extra_lines:
        return content

    print(f"  keep {len(extra_lines)} local-only entries: {local_file}")
    return content.rstrip('\n') + '\n' + '\n'.join(extra_lines)


def sync_file(upstream_file, output_file, dict_data):
    content = build_updated_content(upstream_file, dict_data)
    content = keep_local_only_entries(content, output_file)
    write_file(output_file, content)


def main():
    parser = argparse.ArgumentParser(
        description='同步 rime-frost 词库并追加墨奇码等辅助码')
    parser.add_argument(
        '--upstream-dir',
        default=os.environ.get('RIME_FROST_DIR', r'D:\vscode\rime-frost'),
        help='rime-frost 仓库根目录（默认取环境变量 RIME_FROST_DIR）')
    parser.add_argument(
        '--output-dir',
        default=str(REPO_ROOT),
        help='输出根目录，默认为本仓库根目录')
    args = parser.parse_args()

    upstream_dir = Path(args.upstream_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    upstream_cn_dicts = upstream_dir / 'cn_dicts'
    upstream_cn_dicts_cell = upstream_dir / 'cn_dicts_cell'
    if not upstream_cn_dicts.is_dir():
        raise SystemExit(f'Upstream cn_dicts not found: {upstream_cn_dicts}')

    dict_data = build_dict_data()

    # Test prints
    print("火字的编码测试:")
    print("moqi:", dict_data['moqi'].get('火'))
    print("xh:", dict_data['xh'].get('火'))
    print("zrm:", dict_data['zrm'].get('火'))
    print("hx:", dict_data['hx'].get('火'))

    output_cn_dicts = output_dir / 'cn_dicts'
    output_cn_dicts_cell = output_dir / 'cn_dicts_cell'
    output_cn_dicts.mkdir(parents=True, exist_ok=True)
    output_cn_dicts_cell.mkdir(parents=True, exist_ok=True)

    # Process main files
    print("Processing main dictionary files...")
    for file_name in MAIN_DICT_FILES:
        yaml_file_path = upstream_cn_dicts / file_name
        write_file_path = output_cn_dicts / file_name

        if yaml_file_path.exists():
            sync_file(yaml_file_path, str(write_file_path), dict_data)
        else:
            print(f"File not found: {yaml_file_path}")

    # Process cell dictionary files
    print("Processing cell dictionary files...")
    if upstream_cn_dicts_cell.is_dir():
        for file_name in sorted(os.listdir(upstream_cn_dicts_cell)):
            yaml_file_path = upstream_cn_dicts_cell / file_name
            if not yaml_file_path.is_file() or not file_name.endswith('.yaml'):
                continue
            write_file_path = output_cn_dicts_cell / file_name
            sync_file(yaml_file_path, str(write_file_path), dict_data)
    else:
        print(f"Cell path not found: {upstream_cn_dicts_cell}")


if __name__ == '__main__':
    main()
