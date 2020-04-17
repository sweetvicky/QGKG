import os
import ahocorasick
from py2neo import Graph
import random

class AnswerClassifier:
    def __init__(self):

        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.fit_up_symptom = ['情绪低落', '兴趣减退', '精力丧失', '注意力降低', '自信心丧失', '自责自罪', '前途问题', '自杀', \
                      '睡眠障碍', '食欲改变', '疼痛', '月经问题', '头晕', '虚弱', '心脏问题', '胸闷问题', '性功能障碍', \
                      '排泄不适', '消化不适', '妄想', '幻觉', '抑郁性木僵']

    '''分类主函数'''
    def classify1(self, word_dict, preques_infor):
        medical_dict = self.word_analysis(word_dict)
        data = {}
        # if not medical_dict:
        #     return data,  preques_infor, word_dict

        #收集问句当中所涉及到的实体类型
        # types = []
        # for type_ in medical_dict.keys():
        #     types += type_
        if not medical_dict:
            types = []
        else:
            types = list(medical_dict.keys())


        # 在这里开始是我需要去考虑的东西.在具有了这些东西之后,我如何进行封装。

        preques_type = preques_infor['question_type']
        prediagnosis_infor = preques_infor['diagnosis_infor']

        # 确定下一个问题的类型
        '''
        [在诊断完成之后,再进行修改]
        目前的方案是分为上一个问题是'new_symptom'，还是'spec_symptom',还是'ques_degree'
        如果是'new_symptom',就要将症状词语加上,但结果中如果有两个以上(除症状外两个以上的词)并包括频率的其中一种,就为'new_symptom'。
        否则如果没有频率词就问'ques_degree'，如果只有一个词，那就'spec_symptom'
        如果是'spec_symptom',则需要将症状词语, 程度词语。因为用户肯定会有否定或者肯定回答，因此直接采取'new_symptom'。
        '''
        question_type = ''

        if preques_type == 'new_symptom':
            keynum = len(types) - 1
            # 首先判断有没有症状词,没有症状词，将上个问题的症状词语加上。
            if 'symptom' in types and ('time' in types or 'frequent' in types):
                # 这里要去维护已经完成的诊断列表
                question_type = 'new_symptom'
                preques_infor['question_type'] = question_type
                preques_infor['diagnosis_infor'] = medical_dict
            elif bool(1 - ('symptom' in types)):
                if bool(1 -('symptom' in list(prediagnosis_infor.keys()))):
                    prediagnosis_infor['symptom'] = '情绪低落'
                medical_dict['symptom'] = prediagnosis_infor['symptom']
                word_dict['symptom'] = medical_dict['symptom']
                types.append('symptom')
                keynum += 1
            if question_type == '':
                if 'time' in types or 'frequent' in types:
                # 这里要去维护已经完成的诊断列表
                    question_type = 'new_symptom'
                    preques_infor['question_type'] = question_type
                    preques_infor['diagnosis_infor'] = medical_dict
                else:
                    question_type = 'spec_symptom'
                    preques_infor['question_type'] = question_type
                    # 'spec_symptom'查询要问的子症状
                    sub_symptom = self.search('up_down_symptom', medical_dict['symptom'])
                    data['sub_symptom'] = sub_symptom
                    # 这里不能给那边进行诊断,所以我需要加入进preques_infor列表中
                    medical_dict['sub_symptom'] = sub_symptom
                    medical_dict['time'] = '大部分时间'
                    preques_infor['diagnosis_infor'] = medical_dict

            # # 如果有两个以上(除症状外两个以上的词)的实体(表明可诊断)为'new_symptom',否则为'spec_symptom'
            # if keynum >= 2 and ('frequent' in types):
            #     # 这里要去维护已经完成的诊断列表
            #     question_type = 'new_symptom'
            #     preques_infor['question_type'] = question_type
            #     preques_infor['diagnosis_infor'] = medical_dict
            # else:
            #     question_type = 'spec_symptom'
            #     preques_infor['question_type'] = question_type
            #     # 'spec_symptom'查询要问的子症状
            #     sub_symptom = self.search('up_down_symptom', medical_dict['symptom'])
            #     data['sub_symptom'] = sub_symptom
            #     # 这里不能给那边进行诊断,所以我需要加入进preques_infor列表中
            #     medical_dict ['sub_symptom'] = sub_symptom
            #     medical_dict['time'] = '大部分时间'
            #     preques_infor['diagnosis_infor'] = medical_dict
        elif preques_type == 'spec_symptom':
            pre_medical_dict = preques_infor['diagnosis_infor']
            for k in pre_medical_dict.keys():
                if bool(1-(k in types)) and k != 'denyword':
                    medical_dict[k] = pre_medical_dict[k]
            word_dict['symptom'] = medical_dict['symptom']
            word_dict['sub_symptom'] = medical_dict['sub_symptom']
            # 这种情况直接默认(可诊断)为'new_symptom', 这里要去维护已经完成的诊断列表
            question_type = 'new_symptom'
        elif preques_type == 'ques_degree':
            pre_medical_dict = preques_infor['diagnosis_infor']
            for k in pre_medical_dict.keys():
                if bool(1-(k in types)):
                    medical_dict[k] = pre_medical_dict[k]
            # 这种情况直接默认(可诊断)为'new_symptom', 这里要去维护已经完成的诊断列表
            question_type = 'new_symptom'

        # print('preques_type: %s, question_types: %s.' % (preques_infor['question_type'], question_type))
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_type'] = question_type
        preques_infor['question_type'] = question_type
        return data,  preques_infor, word_dict

    def word_analysis(self,word_result):
        medical_dict = {}
        if word_result['symptoms'] != []:
            sub_symptom = word_result['symptoms'][0]
            print('sub_symptom:' + sub_symptom)
            # 将小症状映射到大症状的过程(利用知识图谱)
            if sub_symptom in self.fit_up_symptom:
                medical_dict['symptom'] = sub_symptom
            else:
                symptom = self.search('down_up_symptom',sub_symptom)[0]
                medical_dict['symptom'] = symptom
        tmplist = ['time','frequent','degree','denyword']
        for i, word in enumerate(word_result['other_words']):
            if word != {}:
                medical_dict[tmplist[i]] = list(word.keys())[0]
        return medical_dict


    def search(self,sql_type, data):
        sql = self.build_sql(sql_type, data)[0]
        ress = self.g.run(sql).data()
        keyword = ''
        if sql_type == 'up_down_symptom':
            down_symptoms = list(set([i['n.name'] for i in ress]))
            if len(down_symptoms) == 1:
                symptoms_num = 1
            else:
                symptoms_num = min(random.randint(2, len(down_symptoms)), 4)
                random.shuffle(down_symptoms)
            keyword = down_symptoms[:symptoms_num]
            # select_symptoms = down_symptoms[:symptoms_num]
            # keyword = '、'.join(select_symptoms)
        elif sql_type == 'down_up_symptom':
            keyword = list(set([i['m.name'] for i in ress]))
        return keyword

    def build_sql(self, sql_type, data):
        sql = []
        datas = [data]
        if sql_type=='down_up_symptom':
            sql = ["MATCH (m:down_symptom)-[r:sub_sub_symptom]->(n:down2_symptom) where n.name = '{0}' return m.name".format(i) for i in datas]
        elif sql_type=='up_down_symptom':
            sql = ["MATCH (m:down_symptom)-[r:sub_sub_symptom]->(n:down2_symptom) where m.name = '{0}' return n.name".format(i) for i in datas]
        return sql


    # def symptom_match(self,types):
    #     # 这里的主要的逻辑是诊断过程中，是否可以匹配上。
    #     if ('symptom' in types) and ('frequent' in types):
    #         return 'full'
    #     elif ('symptom' in types):
    #         return 'no_frequent'
    #     else:
    #         return 'no_symptom'

    '''构造词对应的类型'''
    # def build_wdtype_dict(self):
    #     wd_dict = dict()
    #     for wd in self.region_words:
    #         wd_dict[wd] = []
    #         if wd in self.disease_wds:
    #             wd_dict[wd].append('disease')
    #         if wd in self.drug_wds:
    #             wd_dict[wd].append('drug')
    #         if wd in self.symptom_wds:
    #             wd_dict[wd].append('symptom')
    #         if wd in self.degree_wds:
    #             wd_dict[wd].append('degree')
    #         if wd in self.frequent_wds:
    #             wd_dict[wd].append('frequent')
    #         if wd in self.time_wds:
    #             wd_dict[wd].append('time')
    #         if wd in self.yesno_wds:
    #             wd_dict[wd].append('yesno')
    #
    #
    #     return wd_dict

    '''构造actree，加速过滤'''
    # def build_actree(self, wordlist):
    #     actree = ahocorasick.Automaton()
    #     for index, word in enumerate(wordlist):
    #         actree.add_word(word, (index, word))
    #     actree.make_automaton()
    #     return actree

    # '''问句过滤'''
    # def check_medical(self, question):
    #     region_wds = []
    #     for i in self.region_tree.iter(question):
    #         wd = i[1][1]
    #         region_wds.append(wd)
    #     stop_wds = []
    #     for wd1 in region_wds:
    #         for wd2 in region_wds:
    #             if wd1 in wd2 and wd1 != wd2:
    #                 stop_wds.append(wd1)
    #     final_wds = [i for i in region_wds if i not in stop_wds]
    #     final_dict = {self.wdtype_dict.get(i)[0]:i for i in final_wds}
    #
    #     return final_dict
    #
    # '''基于特征词进行分类'''
    # def check_words(self, wds, sent):
    #     for wd in wds:
    #         if wd in sent:
    #             return True
    #     return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)