#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
"""
构建字典可以忽略
"""
with open( "THUOCL.json", "r") as f:
    typed_words0 = json.load(f)

data=[]
for type0 in typed_words0:
    data=data+typed_words0[type0]
# print("data",len(data))
with  open('dict.txt','w') as f:
    # f.write("\n".join(data))
    for word in data:
        f.write(word+"\n")