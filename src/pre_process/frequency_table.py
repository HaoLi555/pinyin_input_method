import json
import os
from tqdm import tqdm
import argparse
import re

SINA_NEWS_GBK = "/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/语料库/语料库/sina_news_gbk"
SMP2020 = (
    "/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/语料库/语料库/SMP2020"
)
THRESHOLD_VALUE = 10


def is_chn_char(char):
    if "\u4e00" <= char <= "\u9fff":
        return True
    else:
        return False


def build_frequency_table(corpus_tuple, save_path, trigarm):
    """
    corpus_tuple:tuple (flag:int,path:str)
    save_path:str
    trigram:bool
    """
    frequency_table = {}
    for file in os.listdir(corpus_tuple[1]):
        if "README" not in file:
            # 两个语料库文件的编码方式不同
            # TODO:关于第二个文件的处理
            with open(os.path.join(corpus_tuple[1], file), "r", encoding="GBK") as f:
                # 文件过大，分行读入
                corpus = []
                for line in f.readlines():
                    assert corpus_tuple[0] in [1, 2]
                    # 语料库不同，处理方法不同——因为SMP2020使用的是单引号，不能直接json解析
                    if corpus_tuple[0] == 1:
                        dict = json.loads(line)
                        corpus.append(dict)
                    elif corpus_tuple[0] == 2:
                        dict = {
                            "content": re.findall(r"'content': '(.+?)', 'label':", line)
                        }
                        corpus.append(dict)

                for new in tqdm(corpus, desc=f"Processing {file}"):
                    for key in new.keys():
                        if (
                            key == "title" or key == "html" or key == "content"
                        ) and len(new[key]) != 0:
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
                                        word = (
                                            new[key][i]
                                            + new[key][i + 1]
                                            + new[key][i + 2]
                                        )
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
    with open(
        save_path,
        "w",
    ) as savef:
        json.dump(frequency_table, savef, ensure_ascii=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    # NOTE：当前的目录是根目录，这里后续还要修改！
    parser.add_argument(
        "--corpus_path_flag",
        type=int,
        choices=[1, 2],
        default=1,
        help="Corpus file path. 1 stands for sina_news_gbk and 2 stands for SMP2020.",
    )
    parser.add_argument(
        "--frequency_table_path",
        type=str,
        default="src/data/frequency_table.txt",
        help="Frequency table file path.",
    )
    parser.add_argument(
        "--trigram",
        action="store_true",
        help="Whether to generate a trigram model frequency table.",
    )

    args = parser.parse_args()

    # tuple (flag,path) 便于判断当前使用的是哪个语料库
    corpus_tuple = (1, SINA_NEWS_GBK) if args.corpus_path_flag == 1 else (2, SMP2020)
    save_path = args.frequency_table_path
    trigram = args.trigram

    build_frequency_table(
        corpus_tuple=corpus_tuple, save_path=save_path, trigarm=trigram
    )
