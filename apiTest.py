from aip import AipNlp


emotionDic = {'0':'消极','1':'中立','2':'积极'}
class apiTest:
    '''
    用于调百度自然语言处理接口，包括分词、转词向量、文本相似度匹配、评论观点抽取和情感分析
        · segmentation(self, text):分词
        · word2vec(self, text):转词向量
        · similarity(self,text1,text2,option ="BOW"):文本相似度匹配
        · pointExtraction(self,text,option =4):评论观点抽取
        · sentiment(self,text):情感分析
    '''

    def __init__(self):
        self.APP_ID = '18579658'
        self.API_KEY = '6cYCfanilGMEv6pFfGSarCt6'
        self.SECRET_KEY = 'MYSt3G14r4RznDwTMwPPgzQ1bolXIyBY'
        self.client = AipNlp(self.APP_ID, self.API_KEY, self.SECRET_KEY)


    def sentiment(self, text):
        '''
        情感分析
        :param text: 待分析句子
        :return: List, 三个数据，包括情感分类结果、置信度、积极概率
        '''
        response = self.client.sentimentClassify(text)
        if ('error_code' not in response):
            for item in response['items']:
                return [item['sentiment'], item['confidence'], item['positive_prob']]
        return False

    def word2vec(self, text):
        '''
        转词向量
        :param text:只能是 词， 不能是句子
        :return:List, 词向量
        '''
        response = self.client.wordEmbedding(text);
        if ('error_code' not in response):
            return response['vec']
        return False

# if __name__ == '__main__':
#     test = apiTest()
#
#     #  **********  情感评分  ***********
#     print("情感评分".center(50, "*"))
#     text = "食欲增加"
#     result = test.sentiment(text)
#     print("   文本：", text)
#     print("   情感分类：", emotionDic[str(result[0])])
#     print("   置信度：", result[1])
#     print("   积极概率：", result[2])
#     print("   消极概率：", 1 - result[2])
#     print("end".center(54, "-"), "\n")


