from py2neo import Graph
import random

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
        self.num_limit = 50

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, answers, sqls):
        question_type = sqls['question_type']
        queries = sqls['sql']
        if question_type == 'spec_symptom':
            ress = self.g.run(queries).data()
            down_symptoms = list(set([i['n.name'] for i in ress]))
            symptoms_num = min(random.randint(2, len(down_symptoms)),4)
            random.shuffle(down_symptoms)
            select_symptoms = down_symptoms[:symptoms_num]
            keyword = '、'.join(select_symptoms)
            final_answers = answers % keyword
        else:
            final_answers = answers
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        #print(question_type)
        final_answer = []
        if not answers or '' in answers[0].values():#查不到
            return '抱歉，暂时没有相关记载'

        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可能的病因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_treatment':
            desc = [i['m.treatment'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}可以尝试如下治疗方法：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))



        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},解释如下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'symptom_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0},解释如下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_check':
            desc = [i['m.check'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_use':
            desc = [i['m.use'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的用法用量如下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_uneffect':
            desc = [i['m.uneffect'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的不良反应如下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_forbid':
            desc = [i['m.forbid'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的禁忌如下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_attention':
            desc = [i['m.attention'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的注意事项如下：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()