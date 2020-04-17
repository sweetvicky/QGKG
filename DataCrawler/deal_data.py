import os
import re
import jieba
import xlrd
import csv
import pandas

output_file_name="word2vec_train.txt"
output_file = open(output_file_name, 'a', encoding='utf-8')
cn_reg = '^[\u4e00-\u9fa5]+$'
f = open("stopwords.txt", encoding="utf-8")
stopwords = []
lines = f.readlines()
for line in lines:
    stopwords.append(line.split("\n")[0])
f.close()

def collect_txt_data():
    path="爬虫"
    for root, dirs, files in os.walk(path):
        for file in files:
            f = open("爬虫/" + file, encoding='utf-8')
            lines = f.readlines()
            for line in lines:
                line = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！：:，。？、~@#￥%……&*（）]+", " ",line.split('\n')[0])+"\n"#去除符号
                line=' '.join(jieba.cut(line.split('\n')[0].replace(' ', ''))) + '\n'#分词
                line_list = line.split('\n')[0].split(' ')
                line_list_new = []
                for word in line_list:
                    if re.search(cn_reg, word):
                        line_list_new.append(word)
                output_file.write(' '.join(line_list_new) + '\n')

def collect_csv_data():
    path = "DataCrawler"
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            csvfile=open(path+"/"+file,"r",encoding="utf-8")
            reader = csv.reader(csvfile)
            column1 = [row[1] for row in reader]
            for line in column1:
                line = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！：:，。？、~@#￥%……&*（）]+", " ",
                              line.split('\n')[0]) + "\n"  # 去除符号
                line = ' '.join(jieba.cut(line.split('\n')[0].replace(' ', ''))) + '\n'  # 分词
                line_list = line.split('\n')[0].split(' ')
                line_list_new = []
                for word in line_list:
                    if re.search(cn_reg, word):
                        line_list_new.append(word)
                #output_file.write(' '.join(line_list_new) + '\n')
                print(' '.join(line_list_new) + '\n')


def del_stopwords():#word2vec_train.txt是没有去除stopwords的，而ti_idf_train.txt是去除过停用词的
    path = "word2vec_train.txt"
    f=open(path,mode="r",encoding="utf-8")
    lines=f.readlines()
    output=open("ti-idf_train.txt",mode="a",encoding="utf-8")
    for line in lines:
        line_list=line.split("\n")[0].split(' ')
        line_list_new = []
        for word in line_list:
            if word not in stopwords:
                line_list_new.append(word)

        output.write(' '.join(line_list_new) + '\n')
        #print(' '.join(line_list_new) + '\n')




if __name__ == "__main__":
    del_stopwords()