#coding=UTF-8 
import json


# f = open('THUOCL.json',"r")  
with open( "THUOCL.json", "r") as f:
    typed_words0 = json.load(f)
data=[]
for type0 in typed_words0:
    # print("",typed_words0[type0])
    data=data+typed_words0[type0]
print("data",len(data))
f1 = open('/tmp/test.txt','w')
f1.write('hello boy!牛逼')