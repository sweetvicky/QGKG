from aclassifier import *
from atransfer import *
from aresult import *
from extract_answerkey import *
from sim_symptoms import *
from lstm_predict import *
from apiTest import *



import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码
'''问答类'''
class ChatBotGraph:
    def __init__(self):

        self.extract_answerkey = extract_answerkey()
        self.sim_cilin = SimCilin()
        self.lstm_predict = LSTMNER()
        self.apiTest = apiTest()

        self.classifier = AnswerClassifier()
        self.parser = AnswerPaser()
        self.searcher = AnswerSearcher()
        # 10个发作大症状的关键词列表
        self.stopword = "好的,我们已经初步了解了你的情况，现正在进行诊断请稍后......"

    # def chat_main(self, sent, orders):
    #     answer = '抱歉，暂时没有相关记载'
    #     res_classify, orders = self.classifier.classify(sent,wait_symptom)
    #     if not res_classify:
    #         return answer
    #     res_sql = self.parser.parser_main(res_classify, orders)
    #     final_answers = self.searcher.search_main(res_sql)
    #     if not final_answers:
    #         return answer,wait_symptom
    #     else:
    #         return '\n'.join(final_answers),wait_symptom

    def word_vect(self, sent):
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
        # print("结果".center(50, "*"))
        if sentiment_result == False:
            sentiment_result = [2,0.5,0.5]
        if sentiment_result[2]>0.9:#积极
            if len(final_scores)>0:#如果没有匹配到相似症状，则没有必要显示关键词
                result['keyword'] = result_key
                # print("关键词：",result_key)
            # print(("相似的症状的评分: " + str(final_scores)))
            # print(("相似的症状: " + str(res)))
            # print("程度词，时间词，频率词:",other_result)
        # else:
            # print(("相似的症状的评分: " + str(final_scores)))
            # print(("相似的症状: " + str(res)))
            # print("程度词，时间词，频率词:",other_result)
        result['syms_score'] = final_scores
        result['symptoms'] = res
        result['other_words'] = other_result
        # print("end".center(54, "-"))
        return result

    def ques_main(self, sent, wait_symptom, arrive_symptom, preques_infor,diag_list):
        answer = self.stopword
        word_result = self.word_vect(sent)
        res_classify, preques_infor, word_result = self.classifier.classify1(word_result, preques_infor)

        # res_classify, preques_infor = \
            # self.classifier.classify(sent, preques_infor)

        if not res_classify:
            return answer, wait_symptom

        tmp_symptom = preques_infor['diagnosis_infor']['symptom']
        # 如果问题类型为'new_symptom',说明用户回答有效,加入到诊断的列表中,并确定下一个询问的症状(应用wait_symptom, arrive_symptom)
        print('diags:' + str(preques_infor['diagnosis_infor']))
        print('words:' + str(word_result))
        if res_classify['question_type'] == 'new_symptom':
            diag_list['diags'] .append(preques_infor['diagnosis_infor'])
            diag_list['words'].append(word_result)
            #
            # print('diags:' + str(preques_infor['diagnosis_infor']))
            # print('words:' + str(word_result))

            # 更新wait_symptom, arrive_symptom
            if tmp_symptom in arrive_symptom:
                print()
            else:
                arrive_symptom.append(tmp_symptom)
                wait_symptom.remove(tmp_symptom)

            # 检查是否还有需要问的症状,如果没有直接返回
            if wait_symptom == []:
                return answer, wait_symptom, arrive_symptom, preques_infor,diag_list
            else:
                # 确定咨询的症状,即为wait_symptom的第一个
                res_classify['symptom'] = wait_symptom[0]
                preques_infor['diagnosis_infor'] = {}
                preques_infor['diagnosis_infor']['symptom'] = wait_symptom[0]

        # 如果问题类型不为为'new_symptom',说明用户回答需要等待,则preques_infor的症状即延续,作为下一个询问的症状
        else:
            res_classify['symptom'] = tmp_symptom


        final_answers,res_sql = self.parser.get_result(res_classify)

        # final_answers = self.searcher.search_main(answers,res_sql)

        if not final_answers:
            return answer, wait_symptom, arrive_symptom, preques_infor,diag_list
        else:
            return final_answers, wait_symptom, arrive_symptom, preques_infor,diag_list

if __name__ == '__main__':
    handler = ChatBotGraph()
    # 初始化
    fit_up_symptom = ['情绪低落', '兴趣减退', '精力丧失', '注意力降低', '自信心丧失', '自责自罪', '前途问题', '自杀', \
                      '睡眠障碍', '食欲改变', '疼痛', '月经问题', '头晕', '虚弱', '心脏问题', '胸闷问题', '性功能障碍', \
                      '排泄不适', '消化不适', '妄想', '幻觉', '抑郁性木僵']
    # fit_up_symptom = ['情绪低落', '兴趣减退', '精力丧失', '注意力降低', '自信心丧失', '自责自罪', '前途问题', '自杀', '睡眠障碍', '食欲改变']

    diag_list = {}
    diag_list['diags'] = []
    diag_list['words'] = []
    wait_symptom = fit_up_symptom
    arrive_symptom = []
    # 上一个问题的类型
    preques_infor = {'question_type':'new_symptom','diagnosis_infor':{}}
    lists = ['好滴，我最近睡不着觉，经常失眠', '没有，应该还行吧','有时会有心情不好的情况','还行，还是有在坚持', \
             '这个的话，确实不怎么喜欢在人多的地方，更喜欢独处','还可以','嗯嗯，总是感觉异常的疲倦，工作的时候具有注意力挺困难的','嗯嗯，差不多是的', \
             '还行吧','嗯嗯，思维反应更以前比感觉慢了','有些自卑','有的','没有吧，偶尔考虑', \
             '没有','有时会有这样的想法','没有','没有','还行','还行，正常', \
             '还可以', '没有', '没有', '没有', \
             '没有', '应该没有', '没有', '还可以，不会有', '还可以吧', \
             '不会', '嗯嗯，还行', '不会', '没有', \
             '没有', '应该没有', '没有', '正常的吧', '没有', \
             '嗯，应该没有', '没有', '没有', '偶尔会有这样的感觉', \
             '没有', '应该没有', '没有特别思考过', '不是，没有这个症状', '没有', \
             '嗯，应该没有'
             ]
    index = 0
    flag = True
    print('电子医生:你可以先简单陈述你的情况。')
    while flag:
        question = input('用户:')
        # question = lists[index]
        # print('用户:', question)
        answer,wait_symptom,arrive_symptom,preques_infor,diag_list = handler.ques_main \
            (question, wait_symptom, arrive_symptom,preques_infor,diag_list)
        # answer=answer.replace('\xa0’, ’ ')
        index += 1
        print('电子医生:', answer)
        if answer == handler.stopword:
            flag = False
    print('diag_list[\'diags\']:', str(diag_list['diags']))
    print('diag_list[\'words\']:', str(diag_list['words']))