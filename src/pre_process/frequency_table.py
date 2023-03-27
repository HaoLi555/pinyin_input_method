import json
import os
from pathlib import Path
from tqdm import tqdm

# 有无更好的路径表达？
CORPUS_PATH = '/home/haoooooooooooookkkkk/courses/intro_to_AI/big_projects/第一次大作业/语料库/语料库/sina_news_gbk'
SAVE_PATH=Path(os.getcwd()).joinpath('src', 'data', 'frequency_table.txt')

def is_chn_char(char):
    if '\u4e00' <= char <= '\u9fff':
        return True
    else:
        return False


def build_frequency_table():
    frequency_table = {}
    for file in os.listdir(CORPUS_PATH):
        if 'README' not in file:
            with open(os.path.join(CORPUS_PATH, file),'r',encoding='GBK') as f:
                # 文件过大，分行读入
                corpus=[]
                for line in f.readlines():
                    dict=json.loads(line)
                    corpus.append(dict)

                for new in tqdm(corpus,desc=f"Processing {file}"):
                    for key in new.keys():
                        if key == 'title' or key == 'html':
                            for i in range(0, len(new[key]) - 1):
                                if is_chn_char(new[key][i]): 
                                    word = new[key][i] + (new[key][i + 1] if is_chn_char(new[key][i + 1]) else '$')
                                    if word in frequency_table.keys():
                                        frequency_table[word] += 1
                                    else:
                                        frequency_table[word] = 1


    frequency_table={key:value for key,value in frequency_table.items() if value>=3} # 只保留频率较大的
    with open(SAVE_PATH,'w',) as savef:
        json.dump(frequency_table,savef,ensure_ascii=False)


if __name__=='__main__':
    build_frequency_table()