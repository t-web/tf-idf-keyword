#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import re
import datetime
import sys, getopt
from tqdm import tqdm
from segmenter import segment

class MyDocuments(object):    # memory efficient data streaming
    def __init__(self, dirname):
        self.dirname = dirname
        if not os.path.isdir(dirname):
            print(dirname, '- not a directory!')
            sys.exit()
    def sentence_segmentation_v1(self,para):
        """分句函数
        进行精细中文分句（基于正则表达式）

        >>> sentence_segmentation_v1(text)

        """
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        seg=para.split("\n")

        while '' in seg:
            seg.remove('')
        return seg
    def __iter__(self):
        for dirfile in os.walk(self.dirname):
            for fname in dirfile[2]:
                # text = open(os.path.join(dirfile[0], fname),
                #             'r', encoding='utf-8', errors='ignore').read()
                with open(os.path.join(dirfile[0], fname),   'r', encoding='utf-8', errors='ignore') as f:
                    text=''
                    for i,line in enumerate(f):
                        text=text+line
                        if i%1000==0 and i!=0:
                            yield segment(text)   # time consuming
                            text=''




def main(argv):   # idf generator
    inputdir = ''
    outputfile = ''

    usage = 'usage: python gen_idf.py -i <inputdir> -o <outputfile>'
    if len(argv) < 4:
        print(usage)
        sys.exit()
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["idir=","ofile="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:   # parsing arguments
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    documents = MyDocuments(inputdir)

    ignored = {'', ' ', '', '。', '：', '，', '）', '（', '！', '?', '”', '“'}
    id_freq = {}
    i = 0
    for doc in tqdm(documents):
        doc = set(x for x in doc if x not in ignored)
        for x in doc:
            id_freq[x] = id_freq.get(x, 0) + 1
        if i % 1000 == 0:
            print('Documents processed: ', i, ', time: ',
                datetime.datetime.now())
        i += 1

    with open(outputfile, 'w', encoding='utf-8') as f:
        for key, value in id_freq.items():
            f.write(key + ' ' + str(math.log(i / value, 2)) + '\n')


if __name__ == "__main__":
   main(sys.argv[1:])
