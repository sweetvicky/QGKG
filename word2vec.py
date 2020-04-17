from extract_answerkey import *
from sim_symptoms import *
from lstm_predict import *
from apiTest import *


import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码
'''问答类'''
class Wordvect:
    def __init__(self):
        self.extract_answerkey = extract_answerkey()
        self.sim_cilin = SimCilin()
        self.lstm_predict=LSTMNER()
        self.apiTest=apiTest()


    def chat_main(self, sent):
        # 分词结果输出
        result = {}
        # 获取关键词
        result_key=[]
        final_scores=[]
        res=[]
        chars,tags=self.lstm_predict.predict(sent)
        key1=self.lstm_predict.match_key(chars,tags)#提取症状
        if len(key1) != 0:#能提取到症状词，再提取症状修饰词这些
            key2=self.extract_answerkey.ti_idf(sent)
            key=key1+key2
            result_key=list(set(key))#最终关键词
            if "抑郁症" in result_key:#特殊情况处理(抑郁症匹配效果不好，转换为抑郁）
                i=result_key.index("抑郁症")
                result_key[i]="抑郁"
            result_key = list(set(result_key))
            tran_key=(",".join(result_key))#关键词拼接去寻找相似症状

            #获取相似症状
            final_scores,res=self.sim_cilin.key_match_finalkey(tran_key)

        # 获取句子正负情绪，主要用于是否输出关键词
        sentiment_result = self.apiTest.sentiment(sent)

        #获取程度词，时间词，频率词
        other_result=self.extract_answerkey.match_otheranswer(sent)
        print("结果".center(50, "*"))
        print(sentiment_result[2])
        if sentiment_result[2]>0.9:#积极
            if len(final_scores)>0:#如果没有匹配到相似症状，则没有必要显示关键词
                result['keyword'] = result_key
                print("关键词：",result_key)
            print(("相似的症状的评分: " + str(final_scores)))
            print(("相似的症状: " + str(res)))
            print("程度词，时间词，频率词:",other_result)
        else:
            print(("相似的症状的评分: " + str(final_scores)))
            print(("相似的症状: " + str(res)))
            print("程度词，时间词，频率词:",other_result)
        result['syms_score'] = final_scores
        result['symptoms'] = res
        result['other_words'] = other_result
        print("end".center(54, "-"))
        return result
        # return final_scores,res
        # else:
        #     print("抱歉，没有匹配到关键词")




if __name__ == '__main__':
    handler = Wordvect()
    while 1:
        questions = input('用户:')
        handler.chat_main(questions)
        # questions = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！：:，。？、~@#￥%……&*（）]+", " ",
        #               questions)  # 去除符号
        # questions = questions.strip().split(' ')
        # num=0
        # start=time.time()
        # symptoms=dict()
        # for question in questions:
        #     num+=1
        #     print("question:",question)
        #     scores,syms = handler.chat_main(question)
        #     for index in range(len(syms)):#统计所有症状，并选取最高的概率
        #         if syms[index] not in symptoms.keys():
        #             symptoms[syms[index]]=scores[index]
        #         else:
        #             if scores[index]>symptoms[syms[index]]:
        #                 symptoms[syms[index]] = scores[index]
        #     time.sleep(0.2)#避免频繁调用百度接口报错
        #
        # end=time.time()
        # print("问题总数：",num)
        # print("运行时间:%.2f秒" % (end - start))
        #
        # d_order = sorted(symptoms.items(), key=lambda x: x[1], reverse=True)  # 按字典集合中，每一个元组的第二个元素排列。
        # # x相当于字典集合中遍历出来的一个元组。
        # print("症状和评分结果：",d_order)

