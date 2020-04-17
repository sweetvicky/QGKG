#!/usr/bin/env python3
# coding: utf-8

import time
import codecs
import jieba.analyse
import jieba.posseg as pseg
import gensim
import os
import ahocorasick
import heapq
import numpy as np
from numpy.linalg import norm
from apiTest import *





class SimCilin:

    def __init__(self):
        self.cilin_path = 'model/cilin.txt'
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])#os.path.abspath(__file__)返回当前脚本的绝对路径

        #self.sem_dict = self.load_semantic()
        self.model = gensim.models.Word2Vec.load('word2vec_model//test.word2vec')
        #self.model=apiTest()
        self.stopwords = self.create_dict(cur_dir + "词典分类/stopwords.txt")  # 停用词
        self.vocab=self.create_dict(cur_dir+"word2vec_model/vocab.txt")#所有的症状
        filename = "stopwords.txt"
        p = "症状分词.txt"

        jieba.load_userdict(p)
        jieba.analyse.set_stop_words(filename)

    '''创建词典'''

    def create_dict(self, path):
        a = []
        f = open(path, "r", encoding="utf-8")
        lines = f.readlines()
        for line in lines:
            a.append(line.split("\n")[0])
        return (set(a))


    '''求一个list中最大5个值及其索引'''
    def max_number(self,m):
        #m = [9, 8, 8, 6, 6, 5, 4, 2, 2, 0]
        max_num = heapq.nlargest(5, m)
        max_number=[]
        for num in max_num:
            if num >0.5:
                max_number.append(num)
        max_index = []
        for t in max_number:
            #if t>0.5:
            index = m.index(t)
            max_index.append(index)
            m[index] = -1
        return max_number,max_index


    '''比较计算词语之间的相似度，取max最大值'''
    def compute_word_sim(self, word1 , word2):
        # sems_word1 = self.sem_dict.get(word1, [])
        # sems_word2 = self.sem_dict.get(word2, [])
        # #print(sems_word1)
        # #print(sems_word2)
        # score_list = [self.compute_sem(sem_word1, sem_word2) for sem_word1 in sems_word1 for sem_word2 in sems_word2]
        # if score_list:
        #     return max(score_list)
        # else:
        #     return 0
        return self.model.similarity(word1,word2)

    '''基于语义计算词语相似度'''
    def compute_sem(self, sem1, sem2):
        sem1 = [sem1[0], sem1[1], sem1[2:4], sem1[4], sem1[5:7], sem1[-1]]
        sem2 = [sem2[0], sem2[1], sem2[2:4], sem2[4], sem2[5:7], sem2[-1]]
        score = 0
        for index in range(len(sem1)):
            if sem1[index] == sem2[index]:
                if index in [0, 1]:
                    score += 3
                elif index == 2:
                    score += 2
                elif index in [3, 4]:
                    score += 1

        return score

    '''计算两个句子的相似度'''
    def vector_similarity(self,s1, s2):
        def sentence_vector(s):
            word = jieba.lcut(s)
            words=[]
            for w in word:
                if w not in self.stopwords:
                    words.append(w)
            #print("words:",words)
            v = np.zeros(1024)
            for word in words:
                v += self.model.word2vec(word)
            v /= len(words)
            return v

        v1, v2 = sentence_vector(s1), sentence_vector(s2)
        return np.dot(v1, v2) / (norm(v1) * norm(v2))

    '''基于词相似度计算句子相似度'''
    def distance(self, text1, text2):
        # filename = "stopwords.txt"
        # p="症状分词.txt"
        #
        # jieba.load_userdict(p)
        # jieba.analyse.set_stop_words(filename)
        #twords1 = jieba.analyse.extract_tags(text1, topK=3)
        twords1 = []
        word = jieba.lcut(text1)
        for w in word:
            if w not in self.stopwords:
                twords1.append(w)
        twords2 = jieba.analyse.extract_tags(text2, topK=3)

        #print(text1, "分词为:", twords1)
        #print(text2, "分词为:", twords2)

        words1=[]
        words2=[]
        for word in twords1:
            if word in self.vocab:
                words1.append(word)
        for word in twords2:
            if word in self.vocab:
                words2.append(word)

        #print(text1, "分词为:", words1)
        #print(text2, "分词为:", words2)
        if  len(words2)==0:
            return 0

        #words1 = [word.word for word in pseg.cut(text1) if word.flag[0] not in ['u', 'x', 'w']]
        #words2 = [word.word for word in pseg.cut(text2) if word.flag[0] not in ['u', 'x', 'w']]
        # print(text1,"分词为:",words1)
        # print(text2,"分词为:",words2)


        score_words1 = []
        score_words2 = []
        for word1 in words1:
            score = max(self.compute_word_sim(word1, word2) for word2 in words2)
            score_words1.append(score)
        for word2 in words2:
            score = max(self.compute_word_sim(word2, word1) for word1 in words1)
            score_words2.append(score)
        similarity = (sum(score_words1)/len(words1)+sum(score_words2)/len(words2))/2

        #t1=(",".join(words1))
        #t2=(",".join(words2))
        #print(text1, t2)
        #return self.vector_similarity(text1,t2)
        return similarity

    '''用来寻找根据key最相似的几个症状，key是一个由逗号隔开的症状句子'''
    def key_match_finalkey(self,keys):
        #print(keys)
        start = time.time()
        f = open("最终症状.txt", encoding="utf-8")
        d = []
        lines = f.readlines()
        for line in lines:
            d.append(line.split("\n")[0])
        f.close()
        score=[]#用来存储总的1*最终症状的矩阵

        for dd in d:
            t = self.distance(keys, dd)
            score.append(t)
        final_scores,index=self.max_number(score)
        res = []
        for i in index:
            res.append(d[i])
        #print(("相似的症状的评分: " + str(final_scores)))
        #print(("相似的症状: " + str(res)))
        end = time.time()
        #print("本地词典到最终词典匹配运行时间:%.2f秒" % (end - start))
        f.close()
        return(final_scores,res)

def test2(key):
    simer = SimCilin()
    simer.key_match_finalkey(key)


# if __name__ == '__main__':
#     # simer = SimCilin()
#     # simer.key_match_finalkey(["不愿外出"])
#     test2('抑郁症，抑郁')
