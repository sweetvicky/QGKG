import random


class AnswerPaser:

    def __init__(self):

        self.newSymptom_Quewds = ['你最近的%s怎么样呢？','现在还对你以前的%s感兴趣吗？','你的%s有没有明显的变化？', \
                           '你的%s状态还好吗？','你的%s有什么异常表现吗？', \
                           '感觉自己的%s方面最近怎样了？', '会不会考虑%s？', '有没有类似%s的感觉？', \
                           '会产生%s的想法吗？', '试图%s过吗？', '会经常有%s这样子的担心吗？','有没有产生%s？','有没有%s的症状？']
        self.specificSymptom_Quewds = ['会不会时常感觉%s？', '有没有%s, 等这样的症状？', '有%s等类似的感觉吗？', \
                                       '经常有%s等类似的想法？','最近会有%s等表现吗？']
        self.quesDegree_Quewds = ['情况是持续性的吗，是几乎每天都这样吗？', '请问这个症状是反复的吗？']

        self.newconjunc_wds = ['好的,那么', '嗯嗯,明白了.', '这样的话,','了解了,然后', '嗯,好的.那','那']
        self.specconjunc_wds = ['就是说','比如说','好比说','也就是','例如','就像是','譬如','就像','详细来说','详细来说就是']

        self.newSymptom_index = {'情绪低落':{'key':['心情','情绪'],'qindex':[1,3,4,5,6]}, \
                                 '兴趣减退':{'key':['兴趣','爱好'],'qindex':[2,3]}, \
                                 '精力丧失':{'key':['精神','精力'],'qindex':[1,3,4,6]}, \
                                 '注意力降低':{'key':['注意力','决断能力'],'qindex':[1,3,4,6]}, \
                                 '自信心丧失':{'key':['自信力','自信心'],'qindex':[1,3,4]}, \
                                 '自责自罪':{'key':['价值观念','生活意义'],'qindex':[7,8,9]}, \
                                 '前途问题':{'key':['思考自己的前途','想象未来计划'],'qindex':[10,11]}, \
                                 '自杀':{'key':['自残','伤害自己','希望自己死掉','自杀'],'qindex':[8,10,11]}, \
                                 '睡眠障碍':{'key':['睡眠'],'qindex':[1,3,4,6]}, \
                                 '食欲改变': {'key': ['食欲','胃口'], 'qindex': [1, 3, 6]}, \
                                 '疼痛':{'key':['躯体','身体','关节'],'qindex':[1,3,4,6]}, \
                                 '月经问题': {'key': ['经事(限女士回答,男士否定即可)'], 'qindex': [1, 5, 6]}, \
                                 '头晕': {'key': ['脑部功能','头部功能'], 'qindex': [1, 3, 4, 6]}, \
                                 '虚弱': {'key': ['体力','体能'], 'qindex': [1, 3, 4, 6]}, \
                                 '心脏问题': {'key': ['心脏','心口','心脏部位'], 'qindex': [1, 3, 4, 6]}, \
                                 '胸闷问题': {'key': ['呼吸','胸口','胸口部位'], 'qindex': [1, 3, 4, 6]}, \
                                 '性功能障碍': {'key': ['性生活'], 'qindex': [1, 3, 4, 6]}, \
                                 '排泄不适': {'key': ['代谢'], 'qindex': [1, 3, 4, 6]}, \
                                 '消化不适': {'key': ['消化'], 'qindex': [1, 3, 4, 6]}, \
                                 '妄想': {'key': ['妄想'], 'qindex': [8,10]}, \
                                 '幻觉': {'key': ['幻觉'], 'qindex': [12]}, \
                                 '抑郁性木僵': {'key': ['抑郁性木僵'], 'qindex': [13]}
                                 }

        self.specificSymptom_index = {'情绪低落': {'qindex': [2,3,5]}, \
                                 '兴趣减退': {'qindex': [2,5]}, \
                                 '精力丧失': {'qindex': [1,2,3,5]}, \
                                 '注意力降低': {'qindex': [1,2,5]}, \
                                 '自信心丧失': {'qindex': [1,3,4,5]}, \
                                 '自责自罪': {'qindex': [2,3,4,5]}, \
                                 '前途问题': {'qindex': [1,3,4]}, \
                                 '自杀': {'qindex': [3,4,5]}, \
                                 '睡眠障碍': {'qindex': [2,5]}, \
                                 '食欲改变': {'qindex': [2,5]}, \
                                 '疼痛': { 'qindex': [2,3,5]}, \
                                '月经问题': { 'qindex': [2,3,5]}, \
                                '头晕': { 'qindex': [2,3,5]}, \
                                 '虚弱': { 'qindex': [2,3,5]}, \
                                 '心脏问题': { 'qindex': [2,3,5]}, \
                                 '胸闷问题': { 'qindex': [2,3,5]}, \
                                 '性功能障碍': { 'qindex':[2,3,5]}, \
                                 '排泄不适': { 'qindex': [2,3,5]}, \
                                '消化不适': { 'qindex': [2,3,5]}, \
                                '妄想': {'qindex': [2,3,4,5]}, \
                                '幻觉': {'qindex': [2,3,4,5]}, \
                                '抑郁性木僵': {'qindex': [2, 5]}}

    def get_result(self, res_classify):
        sql = {}
        question_type = res_classify['question_type']
        symptom_types = res_classify['symptom']
        sql['question_type'] = question_type
        if question_type == 'new_symptom':
            theSymptom = self.newSymptom_index[symptom_types]
            key_index = random.randint(0,len(theSymptom['key'])-1)
            key_word = theSymptom['key'][key_index]
            conjuc_index = random.randint(0, len(self.newconjunc_wds)-1)
            conjuc_word = self.newconjunc_wds[conjuc_index]
            q_index = random.randint(0,len(theSymptom['qindex'])-1)
            q_word = self.newSymptom_Quewds[int(theSymptom['qindex'][q_index]-1)]
            result0 = q_word % key_word
            result = conjuc_word + result0
            sql['sql'] = ''
        elif question_type == 'spec_symptom':
            theSymptom = self.specificSymptom_index[symptom_types]
            conjuc_index = random.randint(0, len(self.specconjunc_wds) - 1)
            conjuc_word = self.specconjunc_wds[conjuc_index]
            q_index = random.randint(0, len(theSymptom['qindex']) - 1)
            q_word = self.specificSymptom_Quewds[int(theSymptom['qindex'][q_index] - 1)]
            # 这里使用知识图谱去查询小症状
            select_symptoms = res_classify['sub_symptom']
            if len(select_symptoms) == 1:
                keyword = select_symptoms[0]
            else:
                keyword = '、'.join(select_symptoms)
            # sql['sql']  = self.sql_transfer('up_down_symptom', [symptom_types])[0]
            # key_index = random.randint(0, len(theSymptom['key'])-1)
            # key_word = theSymptom['key'][key_index]
            result = (conjuc_word + ',' + q_word) % keyword
        elif question_type == 'ques_degree':
            q_index = random.randint(0, len(self.quesDegree_Quewds)-1)
            result = self.quesDegree_Quewds[q_index]
            sql['sql'] = ''
        return result,sql


    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_type = res_classify['question_type']
        sqls = []
        for question_type in question_type:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_treatment':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_use':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_uneffect':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_forbid':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))

            elif question_type == 'drug_attention':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))


            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'symptom_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 查询大症状有哪些小症状
        if question_type == 'up_down_symptom':
            sql = ["MATCH (m:down_symptom)-[r:sub_sub_symptom]->(n:down2_symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病的原因
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        # 查询疾病的防御措施
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]


        # 查询疾病的治疗方式
        elif question_type == 'disease_treatment':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.treatment".format(i) for i in entities]

        # 查询疾病的相关介绍
        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        #查询症状的介绍
        elif question_type == 'symptom_desc':
            sql = ["MATCH (m:Symptom) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        # 查询疾病有哪些症状
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病常用药品
        elif question_type == 'disease_drug':
            sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]


        # 已知药品查询能够治疗的疾病
        elif question_type == 'drug_disease':
            sql = ["MATCH (m:Disease)-[r:recommend_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 查询疾病应该进行的检查
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.check".format(i) for i in entities]

        # 查询药品的使用说明
        elif question_type == 'drug_use':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.use".format(i) for i in entities]

        # 查询药品的不良反应
        elif question_type == 'drug_uneffect':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.uneffect".format(i) for i in entities]

        # 查询药品的禁忌
        elif question_type == 'drug_forbid':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.forbid".format(i) for i in entities]

        # 查询药品的注意事项
        elif question_type == 'drug_attention':
            sql = ["MATCH (m:Drug) where m.name = '{0}' return m.name, m.attention".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    handler = AnswerPaser()
