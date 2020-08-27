# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:11:11 2020

@author: 12709
"""

import requests
from bs4 import BeautifulSoup

dic_list = []
author_list_total = []
for i in range(30):
    print(str(i)+" iter start:")
    year = 1991+i
    if year < 2000:
        add =  "https://dblp.uni-trier.de/db/conf/ipps/ipps"+str(year)+".html"
    elif year==2004:
        add = "https://dblp.uni-trier.de/db/conf/ipps/ipdps2004-c.html"
    else:
        add = "https://dblp.uni-trier.de/db/conf/ipps/ipdps"+str(year)+".html"
    res = requests.get(add)
    res.encoding = 'utf-8'

    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('.publ-list .entry.inproceedings .data')
    authorlist = []
    for i in range(len(data)):
        num = int((len(data[i])-5)/2)
        for j in range(num-1):
            name = str(data[i].contents[j*2].get_text())
            authorlist.append(name)
            author_list_total.append(name)
    authorlist.sort()
    print("authors_num: " + str(len(authorlist)))
    dic = {}
    pre = ""
    for i in range(len(authorlist)):
        if authorlist[i]==pre:
            dic[pre] = dic[pre]+1
        else:
            pre = authorlist[i]
            dic[pre] = 1
    dic_list.append(dic)
    file_name = "dict"+str(year)
    f = open(file_name,"w",encoding='utf-8')
    f.write(str(dic))
    f.close()
    

author_list_total.sort()
ppre = ""
dic_total = {}
for i in range(len(author_list_total)):
        if author_list_total[i]==ppre:
            dic_total[ppre] = dic_total[ppre]+1
        else:
            ppre = author_list_total[i]
            dic_total[ppre] = 1
end = sorted(dic_total.items(),key = lambda d:(d[1],d[0]), reverse=True)
ff = open("dict_total","w",encoding='utf-8')
ff.write(str(end))
ff.close()


out = open("out.txt", "w",encoding='utf-8')
out.write(" "*80 + "IPDPS HALL OF FAME" + " "*80+"\n")
out.write("-"*180+"\n")
line = "Author"+"\t"*4
for i in range(1991,2021):
    line = line+"' "+str(i)[-2:]+" "
out.write(line+'\n')
out.write('\n')
it = 1
for i in range(len(end)):
    if(end[i][1]<5):
        break
    #num_space = 40-len(end[i][0])
    length = len(end[i][0])
    time = 4-int(length//9)
    lineup = end[i][0]+ "\t"*time#尽量对齐
    for j in range(30):
        if end[i][0] in dic_list[j]:
            lineup = lineup+"|  "+str(dic_list[j][end[i][0]])+"  "
        else:
            lineup = lineup+"|  0  "
    lineup = lineup+ " "*5+"||"+" "*5+str(end[i][1])+"\n"
    out.write(lineup)
    print("iter "+str(it)+" finish")
    it = it+1

out.close()


