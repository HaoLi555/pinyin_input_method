from pathlib import Path
import os
import json

# 路径如何优化
RAW_PINYIN_TABLE_PATH = '/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/拼音汉字表/拼音汉字表/拼音汉字表.txt'
RAW_CHN_CHARS_TABLE_PATH = '/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/拼音汉字表/拼音汉字表/一二级汉字表.txt'
SAVE_PATH = Path(os.getcwd()).joinpath('src', 'data', 'pinyin_table.txt')


def build_pinyin_table():
    with open(RAW_PINYIN_TABLE_PATH, 'r',
              encoding='GBK') as f:  # encoding='GBK'
        with open(RAW_CHN_CHARS_TABLE_PATH, 'r',
                  encoding='GBK') as ref:  # encoding='GBK'
            valid_chn_chars = ref.read()  # 一二级汉字表
            pinyin_table = {}
            for line in f.readlines():
                index = line.find(' ')  # 第一个空格的位置
                pinyin = line[:index]
                chn_chars = [
                    c for c in line[index + 1:]
                    if c != ' ' and c != '\n' and c in valid_chn_chars
                ]  # 汉字列表
                pinyin_table[pinyin] = chn_chars
            with open(SAVE_PATH, 'w') as savef:
                json.dump(pinyin_table, savef,
                          ensure_ascii=False)  # ensure_ascii=False
    return


if __name__ == '__main__':
    build_pinyin_table()