import csv
import math

D_num = 0
other_word = [':','(',')','+','/','&','.']
filter = ['the','a','-','and/or', \
          'as','to','1','2','&','by','in','on','and','of','under','with', \
          'planning','reasoning','problem','solving','method','partial', \
          'learning','model' \
          ]
keywords_pre = []
keywords = []
titles = []
df_dict = {}
keyword_num = {}
tf_dict = {}
Wtd_dict = {}

def get_keywords() :
    with open('AAAI-14 Accepted Papers.csv') as csvfile1:
        csv_reader = csv.DictReader(csvfile1)
        for row in csv_reader:
            global D_num,keyword_num,keywords_pre,keywords
            D_num += 1
            titles.append(row['\ufefftitle'])
            templist=row['keywords'].lower().split()
            for i in templist:
                if i not in filter:
                    if i[-1] in other_word:
                        i = i[:-1]
                    if i[0] == '(':
                        i = i[1:]
                    if i.find(')') != -1:
                        i = i[i.find(')')+1:]
                    if i[-1] =='s' and i[-2]!='s' and i[-2]!= 'i':
                        i = i[:-1]
                    if i.find('process') != -1:
                        i = 'progress'
                    if i.find('model') != -1:
                        i = 'model'
                    if i not in filter and i not in keywords_pre:
                        keywords_pre.append(i)
                        keyword_num[i] = 1
                    elif i not in filter:
                        keyword_num[i] += 1

    for i in keywords_pre:
        if keyword_num[i] > 5:
            df_dict[i] = 0
            keywords.append(i)

    del keywords_pre
    del keyword_num


def get_df():
    with open('AAAI-14 Accepted Papers.csv') as csvfile1:
        csv_reader = csv.DictReader(csvfile1)
        for row in csv_reader:
            for t in keywords:
                if row['\ufefftitle'].lower().find(t) != -1 \
                        or row['keywords'].lower().find(t) != -1 \
                        or row['abstract'].lower().find(t) != -1:
                    df_dict[t] += 1

def get_tf(title_w, keywords_w, abstract_w):
    with open('tf.csv','w') as csvfile4:
        fieldnames = ['\ufefftitle']
        fieldnames += keywords
        csv_writer = csv.DictWriter(csvfile4, fieldnames)
        csv_writer.writeheader()
        with open('AAAI-14 Accepted Papers.csv') as csvfile5:
            csv_reader = csv.DictReader(csvfile5)
            for row in csv_reader:
                a_dict = {}
                a_dict['\ufefftitle'] = row['\ufefftitle']
                for t in keywords:
                    a_dict[t] = \
                        float( \
                            title_w * row['\ufefftitle'].lower().count(t) \
                            + keywords_w * row['keywords'].lower().count(t) \
                            + abstract_w * row['abstract'].lower().count(t)) \
                            /(title_w * (row['\ufefftitle'].count(' ')+1) \
                              + keywords_w * (row['keywords'].count(' ')+1) \
                              + abstract_w * (row['abstract'].count(' ')+1))
                csv_writer.writerow(a_dict)

def get_Wtd():
    with open('tf.csv') as csvfile2:
        csv_reader = csv.DictReader(csvfile2)
        for row in csv_reader:
            templist = []
            for i in keywords:
                if df_dict[i] == 0:
                    templist.append(0)
                else:
                    templist.append(float(row[i]) * math.log(float(D_num)/df_dict[i],2))
            Wtd_dict[row['\ufefftitle']]=templist
            del templist

def calculate(mylambda):
    #mylambda = 0.5 #determined for no reason
    with open('05.csv','w') as csvfile3:
        #fieldnames = ['\ufefftitle']
        #fieldnames += titles
        csv_writer = csv.writer(csvfile3)#,fieldnames)
        #csv_writer.writeheader()
        for a in titles:
            a_dist = []
            #a_dict[a] = 0
            #a_dict['\ufefftitle']= a
            for b in titles:
                if a != b :
                    sum = 0
                    for t in range(len(keywords)):
                        Wm = mylambda * Wtd_dict[a][t]+(1-mylambda)*Wtd_dict[b][t]
                        if Wm != 0:
                            if Wtd_dict[a][t] == 0:
                                sum += (1-mylambda)*(Wtd_dict[b][t]*math.log(Wtd_dict[b][t]/Wm))
                            elif Wtd_dict[b][t] == 0:
                                sum += mylambda * (Wtd_dict[a][t]*math.log(Wtd_dict[a][t]/Wm))
                            else:
                                sum += mylambda * (Wtd_dict[a][t]*math.log(Wtd_dict[a][t]/Wm))+ \
                                       (1-mylambda)*(Wtd_dict[b][t]*math.log(Wtd_dict[b][t]/Wm))
                    a_dist.append(sum)
                else:
                    a_dist.append(0)

            csv_writer.writerow(a_dist)
            del a_dist
def main():
    get_keywords()
    get_df()
    get_tf(3,2,1)
    get_Wtd()
    calculate(0.5)

main()
#the number of group is 22
def check_group():
    num = 0
    with open('AAAI-14 Accepted Papers.csv') as csvfile1:
        csv_reader = csv.DictReader(csvfile1)
        group=[]
        for row in csv_reader:
            i = row['groups'].split()
            for j in i:
                if j.find(')') != -1:
                    tmp = j[1:j.find(')')]
                    if tmp not in group:
                        group.append(tmp)

        for i in group:
            print (i)
        print(len(group))

    print(num)
#check_group()
del keywords
del titles
del df_dict
del tf_dict
del Wtd_dict
