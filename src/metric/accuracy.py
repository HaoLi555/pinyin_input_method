import argparse

def evaluate(output_path,std_output_path):
    out_sentences=[]
    with open(output_path,"r") as output:
        for line in output.readlines():
            out_sentences.append(line.strip())

    std_sentences=[]
    with open(std_output_path,"r") as std_output:
        for line in std_output.readlines():
            std_sentences.append(line.strip())
    
    right_sentence=0 # 正确的句子
    right_char=0 # 正确的字
    tot_char=0 # 总字数
    for i in range(len(std_sentences)):

        if out_sentences[i]==std_sentences[i]:
            right_sentence+=1
            right_char+=len(std_sentences[i])

        else:
            partial_right_char=0 # 这句话中正确的字数
            for j in range(len(std_sentences[i])):
                if out_sentences[i][j]==std_sentences[i][j]:
                    partial_right_char+=1
            right_char+=partial_right_char

        tot_char+=len(std_sentences[i])
    print(f"字准确率：{right_char/tot_char*100}%")
    print(f"句准确率：{right_sentence/len(std_sentences)*100}%")


if __name__=='__main__':

    parser=argparse.ArgumentParser()
    # NOTE：当前的目录是根目录，这里后续还要修改！
    parser.add_argument('--output_path',type=str,default='data/output.txt',help='Output file path.')
    parser.add_argument('--std_output_path',type=str,default='data/std_output.txt',help='Standard output file path.')
    args=parser.parse_args()

    output_path=args.output_path
    std_output_path=args.std_output_path

    evaluate(output_path,std_output_path)

