文件运行方式请直接参见： 二、实验环境
# 拼音输入法

李昊 2021010661

# 一、二元算法

## 1.基本思路与公式推导

### a.隐马尔可夫模型HMM

它用来描述一个含有隐含未知参数的马尔可夫过程。其难点是从可观察的参数中确定该过程的隐含参数。（Wikipedia）

隐藏变量为x，可观察状态为y，每个t时刻的y值仅与x相关，而t时刻的x值与t时刻之前的x值有关。

如下图所示

![HMM](src/pic/HMM.png)

要处理的拼音输入法问题正是HMM的典型问题之一：**解码问题**——已知模型参数，寻找最可能的能产生某一特定输出序列的隐含状态的序列，通常使用**维特比算法**解决。

### b.viterbi算法

考虑字的二元模型。也即认为每一时刻的隐藏状态$x(t)$仅与$x(t-1)$有关，则问题核心即为最大化这样一个概率

$$
P(w_1w_2...w_n)=P(w_1出现的概率)P(w_2|w_1)...P(w_{n}|w_{n-1})
$$

其中$w_i$代表拼音序列中第i个拼音对应的满足要求的汉字，考虑到概率本身可能很小，为了解决它们的乘积下溢的问题，采用**最小化**以下的指标的方法：

$$
-log(P(w_1w_2...w_n))=-log(P(w_1出现的概率))-log(P(w_2|w_1))-...-log(P(w_{n}|w_{n-1}))
$$

对应的维特比算法，在下图中

![veterbi](src/pic/viterbi.png)

只需求出最短路径（此处的路径即为上面的负对数指标），对某一层（第i层，n个元素），由于全局最优一定有局部最优，因此只需考虑前一层（m个元素）已经计算出来的最佳路径——对n个元素中的每一个，计算它与前一层m个元素中的每一个的距离（w）加上前一层已经算出来的局部最优的距离，将其中的最小值赋给当前层的元素，然后在当前层的元素中存下路径——这样从第二层开始的每一层只需计算对应的m*n次，最终复杂度加起来会比蛮力遍历所有路径优得多。

## 2.具体实现

`pinyin.py`

以下讲述处理一个拼音序列的方法

1. 对这个序列中的每一项，查询拼音——汉字字典，每一项拼音可以得到一个列表，整个序列组织成一个list，第i项是第i个拼音对应的可选的汉字的列表。对应`read_pinyin`函数
2. 实现viterbi算法，维护两个list：last_layer以及now_layer，二者的元素都是tuple，具体是(从起点开始的路径也即字符串，路径长度也即指标)，第一层的指标为$-log(字频/总字数)$，之后每一层为 `上一层的最优路径长度+$(-log(AB的次数/A的次数))$` 的最小值。

最终输出最短路径即可

注：

- 阈值选用10
- 平滑处理——当某个频率为0时，赋一个较小的值作为频率。具体为1e-20。
- 总字数TOT_CHAR取为1e10

# 二、实验环境

```cpp
Ubuntu 20.04.3
Linux version 5.10.16.3-microsoft-standard-WSL2 (oe-user@oe-host) (x86_64-msft-linux-gcc (GCC) 9.3.0, GNU ld (GNU Binutils) 2.34.0.20200220) #1 SMP Fri Apr 2 22:23:49 UTC 2021
```

可以参考`requirements.txt`

## 文件目录

```cpp
pinyin_input_method
├─ .gitignore
├─ data
│  ├─ input.txt
│  ├─ output.txt
│  ├─ std_output.txt
│  ├─ trigram_output.txt
│  ├─ trigram_wiki_output.txt
│  └─ wiki_output.txt
├─ requirements.txt
└─ src
   ├─ data
   │  ├─ frequency_table.txt
   │  ├─ pinyin_table.txt
   │  ├─ trigram_frequency_table.txt
   │  ├─ trigram_wiki_frequency_table.txt
   │  └─ wiki_frequency_table.txt
   ├─ metric
   │  └─ accuracy.py
   ├─ pic
   │  ├─ HMM.png
   │  └─ viterbi.png
   ├─ pinyin.py
   └─ pre_process
      ├─ frequency_table.py
      └─ pinyin_table.py
```

- data目录下存储的`std_output.txt`为用于比对的标准答案，`output.txt`与`trigram_output.txt`为sina语料对应的输出，含wiki的对应Wiki语料
- src/data下存放中间结果文件——拼音汉字表、频率表（不含wiki的为sina对应的频率表；不含trigram的存储字和两个字的出现次数，含trigram的存储三个字的出现次数）
- metric用以评价字准确率、句准确率
- pre_process生成中间结果文件
- pinyin.py实现输入法

```cpp
# 一个示例(如果要训练的话)——不能直接运行因为没有语料库，但是中间文件都已附上
python3 src/pre_process/pinyin_table.py
python3 src/pre_process/frequency_table.py --corpus_name SINA --save_path src/data/frequency_table.txt
python3 src/pinyin --input_path data/input.txt --output_path data/output.txt
python3 src/metric/accuracy.py --output_path data/output.txt --std_output_path data/std_output.txt

后面三个文件都有对应的命令行参数可供选择，可用-h查看
```

注：在文件树中

- output.txt为必做的二元sina的输出
- wiki_output.txt为选作的wiki二元的输出
- trigram_output.txt为三元sina的输出
- trigram_wiki_output.txt为三元Wiki的输出

# 三、语料库与数据预处理

- 【必做】新浪新闻2016年的新闻语料库
- 【选做】在GitHub项目nlp_chinese_corpus中选择一个语料库：[https://github.com/brightmart/nlp_chinese_corpus](https://github.com/brightmart/nlp_chinese_corpus)具体来说为**维基百科json版(wiki2019zh)**

## 1.建立拼音汉字表

`src/pre_process/pinyin_table.py`

遍历拼音汉字表，将其组织为一个字典，key为拼音字符串，value为汉字的list，利用json存储字典

存储为`src/data/pinyin_table.txt`

## 2.建立频率表

`src/pre_process/frequency_table.py`

处理语料：

- 二元模型：遍历统计，对每个字统计出现的次数，对相邻（中间只要隔了不是汉字的字符就不算相邻）的两个字统计出现的次数。存储时，所有字都存贮，但是对于**两个字的串**，只存储出现次数大于阈值的。存储为`src/data/frequency_table.txt`或者`src/data/wiki_frequency_table.txt`
- 三元模型：只统计三个字连着出现的次数，大于阈值的存储`src/data/trigram_frequency_table.txt`以及`src/data/trigram_wiki_frequency_table.txt`

# 四、实验效果

- 采用sina新闻语料训练的二元模型——字准确率83.21%，句准确率38.12%
- 采用Wiki语料训练的二元模型——字准确率76.96%，句准确率25.35%

# 五、实例分析

正确实例

1. jing ji jian she he wen hua jian she tu chu le shi ba da jing shen de zhong yao xing 经济建设和文化建设突出了十八大精神的重要性
2. ren gong zhi neng cheng wei zai xian jiao yu ling yu de re ci 人工智能成为在线教育领域的热词
3. zhong guo gong chan dang yuan de chu xin he shi ming shi wei zhong guo ren min mou xing fu wei zhong hua min zu mou fu xing 中国共产党员的初心和使命是为中国人民谋幸福为中华民族谋复兴
4. yin wei hu lian wang gai bian le chuan tong chu ban ye de ying xiao mo shi 因为互联网改变了传统出版业的营销模式
5. zhu bo ni wei shen me bu shuo hua le 主播你为什么不说话了

错误实例

1. 大**的**上的一切都**备**勤劳的双手修饰**的**那么和谐——大地上的一切都被勤劳的双手修饰得那么和谐
2. 我国在外交中一**项议**和平共处五项原则为基本准则——我国在外交中一向以和平共处五项原则为基本准则
3. **还效果**后**硬化**还是开了——海啸过后樱花还是开了
4. 我能**单的气**多大赞美就能**竞得起**多大**的回**——我能担得起多大赞美就能经得起多大诋毁
5. 小猫**苗苗交**——小猫喵喵叫
6. 北京**市**首个举办过夏奥会与冬奥会的城市——北京是首个举办过夏奥会与冬奥会的城市

分析

- **训练语料**对识别的准确有很大影响：正确实例中有许多有关政治、经济的长句识别正确，错误实例中有很多文艺性的、口语化的短句识别错误。这正是因为新闻语料库中的话语大多较为正式，且涉及政治经济等
- **二元算法本身**有局限性：最后一个错误示例中，其实从局部来看输入法做的不错，但是整体看会发现有问题，这说明了二元模型难以处理好**较长上下文**之间的关联

# 六、改进模型

尝试结合字的三元模型

# 0.失败的尝试

使用以下公式

$$
P(w_1w_2...w_n)=P(w_1出现的概率)P(w_2|w_1)P(w_3|w_2w_1)...P(w_{n}|w_{n-1}w_{n-2})
$$

但是求解过程仍然求每一层的最优，下一层在上一层的基础上直接计算：这样实际上不是全局最优

结果：

|  | sina | wiki |
| --- | --- | --- |
| 子准确率 | 69.80% | 61.47% |
| 句准确率 | 38.52% | 25.35% |

## 1.基本思路与公式

同上面的二元模型，只不过是当前认为$x(t)$与$x(t-1),x(t-2)$均有关系

但是如果按照概率累乘的公式直接使用三元模型，算法较为复杂，而且如果遍历整个全空间所需耗时太长。因此考虑使用以下指标作为路径的长度，算法主体上仍然与二元相似——每一层都找最短路径

$$
w=-log(P(w_i|w_{i-1}))*B-log(P(w_i|w_{i-1}w_{i-2}))*T
$$

其中B与T分别表示二元与三元所占的权重。

## 2.具体实现

与二元相似，在pinyin.py中有命令行参数—bigram_weight可以调整二者所占的比重

## 3.测试准确率

| bigram_weight | 0.8 | 0.7 | 0.6 | 0.5 | 0.4 | 0.3 |
| --- | --- | --- | --- | --- | --- | --- |
| 字准确率(sina,wiki)/% | (86.82,81.17) | (87.28,81.64) | (87.39,81.75) | (87.55,82.12) | (87.56,82.43) | (87.66,82.55) |
| 句准确率(sina,wiki)/% | (48.10,31.14) | (49.70,31.94) | (50.90,33.13) | (51.10,34.53) | (51.70,35.13) | (52.69,35.13) |

# 七、参数选择与性能分析

## 1.基于sina的二元模型

| 阈值 | 5000 | 1000 | 100 | 10 |
| --- | --- | --- | --- | --- |
| 小概率 | 1e-10 | 1e-10 | 1e-15 | 1e-15 |
| 字准确率/% | 63.76 | 73.41 | 79.75 | 83.21 |
| 句准确率/% | 12.18 | 20.56 | 31.14 | 38.12 |

由上可见，阈值和小概率结合起来可以提升准确率：

阈值和小概率同时减小时准确率提高——符合直觉，阈值减小意味着信息变多，阈值减小的同时小概率应该减小（因为阈值小之后，表中不包括某一项的概率会变小）

## 2.结合三元的模型

由上上一个表格，

随着三元的比重加大，句准确率变化较为明显——合理的，**因为三元更好地看见全句的关联**。

# 八、语料库的对比

综合上面的表格，sina的表现总是略好于wiki的表现，可能是因为测试的语料与sina更相似，而wiki百科相对正式、官方，导致效果不那么好。可以肯定的是，这两个不同特点的语料更适用于不同的场景下的转换，如果想要做一个各种场景都表现好的输入法需要各种场景的语料。

在wiki结果中“人民群众席问了建”（喜闻乐见），“可比以外去世”（意外去世）可以看出，由于wiki百科涉及到的类似“人民”“社会主义”等经常出现在新浪新闻中的词较少，故翻译失准，另外时间原因（wiki2019）也会导致翻译不对（科比2020年去世）

# 九、总结

结论

- 元数越多，代价越大，效果越好（谷歌好像也才4元，一般小公司好像二元居多）
- 语料库会决定适用的场景，优秀的输入法需要各种语料库都具备
- 参数的调整有些机器学习的思想

可能的改进

- 优选语料、更多语料
- 更多元的模型
- 神经网络、深度学习