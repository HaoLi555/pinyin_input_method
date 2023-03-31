import argparse
import json
import math
from tqdm import tqdm


# NOTE：当前的目录是根目录，这里后续还要修改！
PINYIN_TABLE_PATH='src/data/pinyin_table.txt'
FREQUENCY_TABLE_PATH='src/data/frequency_table.txt'
INPUT_PATH=''
OUTPUT_PATH=''
pinyin_table={}
frequency_table={}

# DEFAULT_CHAR_COUNT=1
# DEFAULT_WORD_COUNT=1
SMALL_PROBABILITY=1e-10
TOT_CHAR=10_000_000_000

def read_pinyin():
    input_pinyin=[]# 需要转换的拼音
    with open(INPUT_PATH,'r') as readf:
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

def pinyin_to_chn_chars(input_pinyin):
    
    chn_output=[]
    for pinyin_sentence in tqdm(input_pinyin,desc="Processing sentences"):
        words_sequence=[]
        for pinyin in pinyin_sentence:
            assert pinyin in pinyin_table.keys()
            words_sequence.append(pinyin_table[pinyin])
        

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
                        # 此时的j的结构：(几个字的str，-log)
                        # NOTE:为0时的处理：给一个小概率
                        metric=-math.log(frequency_table[j[0][-1]+i]/frequency_table[j[0][-1]])+j[1] if j[0][-1]+i in frequency_table.keys()  else -math.log(SMALL_PROBABILITY)+j[1]
                        
                        if metric<=metric_max[1] or metric_max[1]==-1:
                            metric_max=(j[0]+i,metric)

                    now_layer.append(metric_max)
                last_layer=now_layer
                now_layer=[]

        chn_sentence=min(last_layer,key=lambda x:x[1])[0]
        chn_output.append(chn_sentence)
    

    with open(OUTPUT_PATH,'w') as f:
        f.write(chn_output[0])
        for i in range(1,len(chn_output)):
            f.write('\n'+chn_output[i])




if __name__=='__main__':

    parser=argparse.ArgumentParser()
    # NOTE：当前的目录是根目录，这里后续还要修改！
    parser.add_argument('--input_path',type=str,default='data/input.txt',help='Input file path.')
    parser.add_argument('--output_path',type=str,default='data/output.txt',help='Output file path.')
    args=parser.parse_args()

    INPUT_PATH=args.input_path
    OUTPUT_PATH=args.output_path

    with open(PINYIN_TABLE_PATH,'r') as f:
        pinyin_table=json.load(f)
    with open(FREQUENCY_TABLE_PATH,'r') as f:
        frequency_table=json.load(f)

    input_pinyin=read_pinyin()
    pinyin_to_chn_chars(input_pinyin)






    
    