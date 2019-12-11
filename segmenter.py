#!/usr/bin/python
# -*- coding: utf-8 -*-

# import jieba
import re
# jieba.load_userdict("dict.txt")

import pkuseg

# #希望分词时用户词典中的词固定不分开
# lexicon = ['北京大学', '北京天安门']
# #加载模型，给定用户词典
# seg = pkuseg.pkuseg(user_dict=lexicon)
# text = seg.cut('我爱北京天安门')
# print(text)


f = open("dict.txt","r")   
lines = f.readlines()      #读取全部内容 ，并以列表方式返回  
SEG = pkuseg.pkuseg(user_dict=lines)
text = SEG.cut('柯基犬是个小短腿')
print(text)
def segment(sentence, cut_all=False):
    sentence = sentence.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
    # seg = pkuseg.pkuseg(user_dict=lexicon)
    # sentence = ' '.join(jieba.cut(sentence, cut_all=cut_all))
    #对input.txt的文件分词输出到output.txt中，使用默认模型和词典，开20个进程
    sentence = ' '.join(SEG.cut(sentence))
    return re.sub('[a-zA-Z0-9.。:：,，)）(（！!??”“\"]', '', sentence).split()
