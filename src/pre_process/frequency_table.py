import json
import os
from tqdm import tqdm
import argparse
import re

SINA_NEWS_GBK = "/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/语料库/语料库/sina_news_gbk"
WIKI = "/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/语料库/语料库/wiki_zh_2019/wiki_zh"
THRESHOLD_VALUE = 10


def is_chn_char(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def process_corpus(corpus_list, keys, trigram):
    frequency_table = {}
    for new in tqdm(corpus_list, desc=f"Processing file"):
        for key in new.keys():
            if key in keys and len(new[key]) != 0:
                # 二元模型：统计单个字以及两个字
                if not trigram:
                    for i in range(0, len(new[key]) - 1):
                        if is_chn_char(new[key][i]):
                            # 如果能构成一个词，测统计词出现的频率
                            if is_chn_char(new[key][i + 1]):
                                word = new[key][i] + new[key][i + 1]
                                if word in frequency_table.keys():
                                    frequency_table[word] += 1
                                else:
                                    frequency_table[word] = 1

                            # 统计一个字出现的频率
                            char = new[key][i]
                            if char in frequency_table.keys():
                                frequency_table[char] += 1
                            else:
                                frequency_table[char] = 1

                    # 处理最后一个字
                    char = new[key][-1]
                    if char in frequency_table.keys():
                        frequency_table[char] += 1
                    else:
                        frequency_table[char] = 1
                # 三元模型：只统计三个字
                else:
                    for i in range(0, len(new[key]) - 2):
                        if (
                            is_chn_char(new[key][i])
                            and is_chn_char(new[key][i + 1])
                            and is_chn_char(new[key][i + 2])
                        ):
                            word = new[key][i] + new[key][i + 1] + new[key][i + 2]
                            if word in frequency_table.keys():
                                frequency_table[word] += 1
                            else:
                                frequency_table[word] = 1
    # 只保留频率较大的词，保留所有的字
    frequency_table = {
        key: value
        for key, value in frequency_table.items()
        if len(key) == 1 or value >= THRESHOLD_VALUE
    }
    return frequency_table


def load_corpus(corpus_name):
    """
    pram: corpus_name:str
    return: list of dict
    """
    assert corpus_name in ["SINA", "WIKI"]
    corpus_list = []
    if corpus_name == "SINA":
        for file in os.listdir(SINA_NEWS_GBK):
            if "README" not in file:
                with open(os.path.join(SINA_NEWS_GBK, file), "r", encoding="GBK") as f:
                    # 文件过大，分行读入
                    for line in f.readlines():
                        corpus_dict = json.loads(line)
                        corpus_list.append(corpus_dict)
    if corpus_name == "WIKI":
        for dir in os.listdir(WIKI):
            dir_path = os.path.join(WIKI, dir)
            for file in os.listdir(dir_path):
                # utf-8编码
                with open(os.path.join(dir_path, file), "r") as f:
                    # 文件过大，分行读入
                    for line in f.readlines():
                        corpus_dict = json.loads(line)
                        corpus_list.append(corpus_dict)

    return corpus_list


def build_frequency_table(corpus_name, save_path, trigarm):
    """
    corpus_name:str
    save_path:str
    trigram:bool
    """
    assert corpus_name in ["SINA", "WIKI"]
    corpus_list = load_corpus(corpus_name=corpus_name)
    # 需要用到的字典键——特定于语料库
    keys = []
    if corpus_name == "SINA":
        keys = ["title", "html"]
    if corpus_name == "WIKI":
        keys = ["title", "text"]

    frequency_table = process_corpus(
        corpus_list=corpus_list, keys=keys, trigram=trigarm
    )

    with open(
        save_path,
        "w",
    ) as savef:
        json.dump(frequency_table, savef, ensure_ascii=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--corpus_name",
        type=str,
        choices=["SINA", "WIKI"],
        default="SINA",
        help="Corpus name. SINA stands for sina_news_gbk and WIKI stands for wiki.",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default="src/data/frequency_table.txt",
        help="Frequency table file path.",
    )
    parser.add_argument(
        "--trigram",
        action="store_true",
        help="Whether to generate a trigram model frequency table.",
    )
    parser.add_argument(
        "--sina_path", default=SINA_NEWS_GBK, help="The sina_news_gbk corpus path."
    )
    parser.add_argument(
        "--wiki_path", default=WIKI, help="The wiki_zh_2019 corpus path."
    )

    args = parser.parse_args()

    SINA_NEWS_GBK = args.sina_path
    WIKI = args.wiki_path

    corpus_name = args.corpus_name
    save_path = args.save_path
    trigram = args.trigram

    build_frequency_table(corpus_name=corpus_name, save_path=save_path, trigarm=trigram)
