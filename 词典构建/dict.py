#-*-coding:utf-8-*-
import csv
import ahocorasick

#描述时间
recent=[]
furthest=[]

#描述频率
fre_high=[]
fre_low=[]

def create_dict():
    csvfile = open("时间新.csv", encoding="gbk")
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1]=="recent":
            recent.append(row[0])
        else:
            furthest.append(row[0])
    csvfile.close()
    csvfile = open("频率.csv", encoding="gbk")
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] == "numotherfrequencyhigh" or row[1] == "adfrequencyhigh" or row[1] == "afrequencyhigh":
            fre_high.append(row[0])
        elif row[1] =="numotherfrequencylow" or row[1] == "adfrequencylow ":
            fre_low.append(row[0])
    csvfile.close()
    #print(recent,furthest,fre_high,fre_low)
def create_deny():
    csvfile = open("肯定否定.csv", encoding="gbk")
    reader = csv.reader(csvfile)
    a=[]
    for row in reader:
        if row[1] == "denydes":
            a.append(row[0])
    csvfile.close()
    a=set(a)
    path3 = "../词典分类//否定//否定.txt"
    output_file = open(path3, "a+",encoding="utf-8")
    for l in a:
        output_file.write(l + '\n')


def build_actree(wordlist):
    actree = ahocorasick.Automaton()
    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    return actree

def check_medical(actree,question,wordlist):

    wd_dict = dict()
    for wd in wordlist:
        wd_dict[wd] = []
        if wd in recent:
            wd_dict[wd].append('recent')
        if wd in furthest:
            wd_dict[wd].append('furthest')
        if wd in fre_high:
            wd_dict[wd].append('fre_high')
        if wd in fre_low:
            wd_dict[wd].append('fre_low')

    region_wds = []
    for i in actree.iter(question):
        wd = i[1][1]
        region_wds.append(wd)
    stop_wds = []
    for wd1 in region_wds:
        for wd2 in region_wds:
            if wd1 in wd2 and wd1 != wd2:
                stop_wds.append(wd1)
    final_wds = [i for i in region_wds if i not in stop_wds]
    final_dict = {i: wd_dict.get(i) for i in final_wds}
    return final_dict

if __name__ == "__main__":
    # str=input("输入:")
    # create_dict()
    # wordlist=set(recent+furthest+fre_high+fre_low)
    # actree=build_actree(wordlist)
    # print(check_medical(actree,str,wordlist))
    create_deny()