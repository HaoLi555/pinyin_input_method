import argparse
import json
import math
from tqdm import tqdm


# NOTE：当前的目录是根目录，这里后续还要修改！
PINYIN_TABLE_PATH='src/data/pinyin_table.txt'


pinyin_table={}
frequency_table={}
trigram_frequency_table={}


SMALL_PROBABILITY=1e-20
TOT_CHAR=10_000_000_000

def read_pinyin(input_path):
    input_pinyin=[]# 需要转换的拼音
    with open(input_path,'r') as readf:
        lines=readf.readlines()
        lines[-1]+='\n' # 为了处理最后一个拼音
        for line in lines:
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

def pinyin_to_chn_chars(input_pinyin,trigram):
    
    chn_output=[]
    for pinyin_sentence in tqdm(input_pinyin,desc="Processing sentences"):
        words_sequence=[]
        for pinyin in pinyin_sentence:
            assert pinyin in pinyin_table.keys()
            words_sequence.append(pinyin_table[pinyin])
        
        # 每一层的结构：list内嵌套tuple:(字符串，指标)
        last_layer=[] # 上一层
        now_layer=[] # 当前层
        # NOTE：平滑处理的优化
        for index,words in tqdm(enumerate(words_sequence),desc="Processing words"):
            if index==0:
                # NOTE:平滑处理：对为0的给一个小概率
                now_layer=[(words[i],-math.log(frequency_table[words[i]]/TOT_CHAR)) if words[i] in frequency_table.keys() else(words[i],-math.log(SMALL_PROBABILITY))
                           
                           for i in range(len(words))] 
                
                last_layer=now_layer
                now_layer=[]


            else:
                for i in words:
                    metric_max=('',-1)
                    for j in last_layer:

                        # NOTE:为0时的处理：给一个小概率
                        # 二元模型
                        if not trigram or index==1:
                            metric=-math.log(frequency_table[j[0][-1]+i]/frequency_table[j[0][-1]])+j[1] if j[0][-1]+i in frequency_table.keys()  else -math.log(SMALL_PROBABILITY)+j[1]
                        else:
                            metric=-math.log(trigram_frequency_table[j[0][-2:]+i]/frequency_table[j[0][-2:]])+j[1] if j[0][-2:]+i in trigram_frequency_table.keys()  else -math.log(SMALL_PROBABILITY)+j[1]

                        if metric<=metric_max[1] or metric_max[1]==-1:
                            metric_max=(j[0]+i,metric)

                    now_layer.append(metric_max)
                last_layer=now_layer
                now_layer=[]

        chn_sentence=min(last_layer,key=lambda x:x[1])[0]
        chn_output.append(chn_sentence)
    
    return chn_output






if __name__=='__main__':

    parser=argparse.ArgumentParser()
    # NOTE：当前的目录是根目录，这里后续还要修改！
    parser.add_argument('--input_path',type=str,default='data/input.txt',help='Input file path.')
    parser.add_argument('--output_path',type=str,default='data/output.txt',help='Output file path.')
    parser.add_argument('--trigram',action='store_true',help='Whether to use a trigram model.')
    parser.add_argument('--frequency_table_path',type=str,default='src/data/frequency_table.txt',help='Path of frequency table file.')
    parser.add_argument('--trigram_frequency_table_path',type=str,default='src/data/trigram_frequency_table.txt',help='Path of trigram frequency table file.')

    args=parser.parse_args()

    input_path=args.input_path
    output_path=args.output_path
    trigram=args.trigram
    frequency_table_path=args.frequency_table_path
    trigram_frequency_table_path=args.trigram_frequency_table_path

    with open(PINYIN_TABLE_PATH,'r') as f:
        pinyin_table=json.load(f)
    with open(frequency_table_path,'r') as f:
        frequency_table=json.load(f)
    if trigram:
        with open(trigram_frequency_table_path,'r') as f:
            trigram_frequency_table=json.load(f)

    input_pinyin=read_pinyin(input_path=input_path)
    chn_output=pinyin_to_chn_chars(input_pinyin,trigram=trigram)

    with open(output_path,'w') as f:
        f.write(chn_output[0])
        for i in range(1,len(chn_output)):
            f.write('\n'+chn_output[i])






    
    