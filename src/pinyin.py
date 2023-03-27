import argparse
import json
import math


# NOTE：当前的目录是根目录，这里后续还要修改！
PINYIN_TABLE_PATH='src/data/pinyin_table.txt'
FREQUENCY_TABLE_PATH='src/data/frequency_table.txt'
INPUT_PATH=''
OUTPUT_PATH=''
pinyin_table={}
frequency_table={}

def read_pinyin():
    input_pinyin=[]# 需要转换的拼音
    with open(INPUT_PATH,'r') as readf:
        for line in readf.readlines():
            pinyin_sentence=[]
            pinyin=""
            for i in line:
                if i!=' ' and i!='\n':
                    pinyin+=i
                else:
                    pinyin_sentence.append(pinyin)
                    pinyin=""
            input_pinyin.append(pinyin_sentence)
    return input_pinyin

def pinyin_to_chn_chars(input_pinyin):
    for pinyin_sentence in input_pinyin:
        words_sequence=[]
        for pinyin in pinyin_sentence:
            assert pinyin in pinyin_table.keys()
            words_sequence.append(pinyin_table[pinyin])
        
        # NOTE：如果这里不定义会不会有问题？
        last_layer=[]
        now_layer=[]
        # NOTE：暂未考虑光滑性的问题
        for index,words in enumerate(words_sequence):
            if index==1:
                tot_count=0 # 总出现次数：所有同音字
                count=[] # 每个字分别的出现次数
                for i in words:
                    this_count= sum([num for key,num in frequency_table.items() if i==key[0]])
                    count.append[this_count]
                    tot_count+=this_count
                now_layer=[(words[i],count[i]/tot_count) for i in range(len(count))] # 层的结构是tuple(path:str,metric)的list
                last_layer=now_layer
            else:
                for i in words:
                    for j in last_layer:
        

        # TODO:1.如果某个字没找到的情形完善修改   2.补全后面的处理   3.-log函数



if __name__=='__main__':

    parser=argparse.ArgumentParser()
    # @note：当前的目录是根目录，这里后续还要修改！
    parser.add_argument('--input_path',type=str,default='data/input.txt',help='Input file path.')
    parser.add_argument('--output_path',type=str,default='data/output.txt',help='Output file path.')
    args=parser.parse_args()

    INPUT_PATH=args.input_path
    OUTPUT_PATH=args.output_path

    with open(PINYIN_TABLE_PATH,'r',encoding='GBK') as f:
        pinyin_table=json.load(f)
    with open(FREQUENCY_TABLE_PATH,'r',encoding='GBK') as f:
        frequency_table=json.load(f)







    
    