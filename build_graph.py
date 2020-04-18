# 导入Flask类
from flask import Flask
from datetime import timedelta
from flask import render_template
from flask import request
import os
import re
from pyecharts import options as opts
from pyecharts.charts import Graph, Page
import xlrd
from create_echarts import CreateEcharts
from main import ChatBotGraph

# from aclassifier import *
# from atransfer import *
# from aresult import *
# from extract_answerkey import *
# from sim_symptoms import *
# from lstm_predict import *
# from apiTest import *


# 实例化，可视为固定格式
app = Flask(__name__,template_folder=".")#将默认路径转化为当前文件所在路径


fit_up_symptom = ['情绪低落', '兴趣减退', '精力丧失', '注意力降低', '自信心丧失', '自责自罪', '前途问题', '自杀', '睡眠障碍', '食欲改变']
diag_list = {}
diag_list['diags'] = []
diag_list['words'] = []
arrive_symptom = []
wait_symptom = fit_up_symptom
preques_infor = {'question_type':'new_symptom','diagnosis_infor':{}}
stopword = "好滴,我们已经初步了解了你的情况，初步诊断请稍后......"


# 配置路由，当请求get.html时交由get_html()处理
@app.route('/index.html')
def get_html():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index.html')

@app.route('/index1.html')
def get_html1():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index1.html')

@app.route('/index2.html')
def get_html2():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index2.html')

@app.route('/index3.html')
def get_html3():
    # 使用render_template()方法重定向到templates文件夹下查找get.html文件
    return render_template('templates/index3.html')


# 配置路由，当请求deal_request时交由deal_request()处理
# 默认处理get请求，我们通过methods参数指明也处理post请求
# 当然还可以直接指定methods = ['POST']只处理post请求, 这样下面就不需要if了
class JsCode:
    def __init__(self, js_code: str):
        self.js_code = "--x_x--0_0--" + js_code + "--x_x--0_0--"

    def replace(self, pattern: str, repl: str):
        self.js_code = re.sub(pattern, repl, self.js_code)
        return self

@app.route('/deal_question', methods = ['GET', 'POST'])
def deal_question():
    get_q = request.args.get("q", "")
    handler = ChatBotGraph()
    answer=handler.chat_main(get_q)
    return render_template("templates/index2.html", question=get_q,result=answer)

@app.route('/deal_answer', methods = ['GET', 'POST'])
def deal_answer():
    get_q = request.args.get("q", "")
    handler = ChatBotGraph()
    global wait_symptom, arrive_symptom, preques_infor, diag_list
    answer, wait_symptom, arrive_symptom, preques_infor, diag_list = handler.ques_main \
        (get_q, wait_symptom, arrive_symptom, preques_infor, diag_list)
    # answer, wait_symptom, arrive_symptom, preques_infor, diag_list = ques_main \
    #     (get_q, wait_symptom, arrive_symptom, preques_infor, diag_list)
    return render_template("templates/index3.html", question=get_q,result=answer)


@app.route('/deal_request', methods = ['GET', 'POST'])
def deal_request():

    nodes=[]
    links=[]
    center_name = request.args.get("name", "")
    id= request.args.get("id", "")
    url="templates//render"+str(id)+".html"
    print("tent",center_name)
    file_name = 'kgdata//dataset.xls'
    excel_file = os.getcwd() + '\\' + file_name
    rdata = xlrd.open_workbook(excel_file)
    bool=0
    for i in range(rdata.nsheets):
        table = rdata.sheets()[i]
        for j in range(table.nrows):
            if table.row_values(j)[0]==center_name:
                center_type=table.row_values(0)[0]
                bool=1
                break
        if bool:
            break
    if bool ==0:#代表这是一个单独的节点，不存在他与别的节点存在他是主语的情况，只存在他是别的数据的宾语
        bool2=0
        for i in range(rdata.nsheets):#寻找单独节点类型
            table = rdata.sheets()[i]
            for j in range(table.nrows):
                if table.row_values(j)[2] == center_name:
                    center_type = table.row_values(0)[2]
                    bool2 = 1
                    break
            if bool2:
                break
        categories = []  # 存储与center_name有关系的数据的类型
        categories.append({})
        categories.append({'name': center_type})
        nodes.append({"name": center_name, "des": "name:" + center_name + "<br>type:"+center_type, "category":categories.index({'name':center_type}) , "symbolSize": 100})
        links=[]
        c = (
            Graph(init_opts=opts.InitOpts(width="100%", height="700px"))
                .add("", nodes, links, categories=categories,
                     repulsion=2500, edge_length=150, label_opts=opts.LabelOpts(position="inside", formatter=JsCode(
                    """function (x) { var strs = x.data.name;                   if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                     tooltip_opts=opts.TooltipOpts(formatter=JsCode(
                         """function (x) { if(x.dataType === 'edge'){var strs = x.data.target;   var str = ''; for(var i = 0, s; s = strs[i++];) {  str += s; if(!(i % 40)) str += '<br>'; } return x.data.name+':'+str;} var strs = x.data.des.split('<br>')[0];  var str = ''; for(var i = 0, s; s = strs[i++];) {  str += s; if(!(i % 40)) str += '<br>'; } return str+'<br>'+x.data.des.split('<br>')[1];}""").js_code),
                     edge_label=opts.LabelOpts(position="",
                                               formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                     edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                     )
                .set_global_opts(title_opts=opts.TitleOpts(title=center_name + "相关知识图谱"))

        )
        c.render(path=url)
        return render_template(url)


    print(center_name,center_type)
    data_line=[]
    spo_data=[]#存储所有的与center_name有关系的数据
    for i in range(rdata.nsheets):
        table = rdata.sheets()[i]
        for j in range(table.nrows):
            if table.row_values(j)[0]==center_name and table.row_values(j)[2]!="none":
                data_line=table.row_values(j)
                data_line.append(table.row_values(0)[2])
                print(data_line)
                spo_data.append(data_line)
    types=set()
    types.add(center_type)
    for i in range(len(spo_data)):
        types.add(spo_data[i][3])
    relation_types=set()
    for i in range(len(spo_data)):
        relation_types.add(spo_data[i][1])
    print(types)
    print(relation_types)
    categories = []#存储与center_name有关系的数据的类型
    categories.append({})
    for x in types:
        categories.append({'name': x})

    print(categories)
    nodes.append({"name": center_name+"|"+center_type, "des": "name:" + center_name + "<br>type:"+center_type, "category":categories.index({'name':center_type}) , "symbolSize": 90})
    for x in relation_types:
        nodes.append({"name": x+"|centernode", "des": "", "symbolSize": 30})

    for i in range(len(spo_data)):
        node={"name": spo_data[i][2]+"|"+spo_data[i][3], "des": "name:" + spo_data[i][2] + "<br>type:" + spo_data[i][3],
                      "category": categories.index({'name': spo_data[i][3]}), "symbolSize": 70}
        if node not in nodes:
            nodes.append(node)
    print(nodes)#nodes创建完成

    for x in relation_types:
        links.append({"source": center_name+"|"+center_type, "target": x+"|centernode",
                      "name": x})

    for i in range(len(spo_data)):
        links.append({"source": spo_data[i][1]+"|centernode", "target": spo_data[i][2]+"|"+spo_data[i][3],
                      "name": " "})
    c = (
        Graph(init_opts=opts.InitOpts(width="100%", height="700px"))
            .add("", nodes, links, categories=categories,
                 repulsion=2500, label_opts=opts.LabelOpts(position="inside",formatter=JsCode("""function (x) { var strs = x.data.name;   var n='';    var str='centernode';   if(strs.search(str)!=-1) {return  n;}   var strs = x.data.name.split('|')[0];  if(strs.length<=6){                       return strs;                   }else {                       name = strs.slice(0,6) + '...';                        return name;                   }}""").js_code),
                 tooltip_opts=opts.TooltipOpts(formatter=JsCode("""function (x) { if(x.dataType === 'edge'){return x.data.name;} var strs = x.data.des.split('<br>')[0];  var str = ''; for(var i = 0, s; s = strs[i++];) {  str += s; if(!(i % 40)) str += '<br>'; } return str+'<br>'+x.data.des.split('<br>')[1];}""").js_code),
                 edge_label=opts.LabelOpts(position="",formatter=JsCode("""function (x) {return x.data.name;}""").js_code),
                 edge_symbol=['circle', 'arrow'], edge_symbol_size=[4, 10], is_focusnode="true"
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title=center_name+"相关知识图谱"))

    )
    c.render(path=url)
    return render_template(url)

# def ques_main(sent, wait_symptom, arrive_symptom, preques_infor,diag_list):
#     answer = stopword
#     word_result = word_vect(sent)
#     res_classify, preques_infor, word_result = classifier.classify1(word_result, preques_infor)
#     # res_classify, preques_infor = \
#     # classifier.classify(sent, preques_infor)
#     if not res_classify:
#         return answer, wait_symptom
#
#     tmp_symptom = preques_infor['diagnosis_infor']['symptom']
#     # 如果问题类型为'new_symptom',说明用户回答有效,加入到诊断的列表中,并确定下一个询问的症状(应用wait_symptom, arrive_symptom)
#     print('diags:' + str(preques_infor['diagnosis_infor']))
#     print('words:' + str(word_result))
#
#     if res_classify['question_type'] == 'new_symptom':
#         diag_list['diags'].append(preques_infor['diagnosis_infor'])
#         diag_list['words'].append(word_result)
#         #
#         # print('diags:' + str(preques_infor['diagnosis_infor']))
#         # print('words:' + str(word_result))
#
#         # 更新wait_symptom, arrive_symptom
#         if tmp_symptom in arrive_symptom:
#             print()
#         else:
#             arrive_symptom.append(tmp_symptom)
#             wait_symptom.remove(tmp_symptom)
#
#         # 检查是否还有需要问的症状,如果没有直接返回
#         if wait_symptom == []:
#             return answer, wait_symptom, arrive_symptom, preques_infor, diag_list
#         else:
#             # 确定咨询的症状,即为wait_symptom的第一个
#             res_classify['symptom'] = wait_symptom[0]
#             preques_infor['diagnosis_infor'] = {}
#             preques_infor['diagnosis_infor']['symptom'] = wait_symptom[0]
#
#     # 如果问题类型不为为'new_symptom',说明用户回答需要等待,则preques_infor的症状即延续,作为下一个询问的症状
#     else:
#         res_classify['symptom'] = tmp_symptom
#
#     final_answers,res_sql = parser.get_result(res_classify)
#
#     # final_answers = searcher.search_main(answers,res_sql)
#
#     if not final_answers:
#         return answer, wait_symptom, arrive_symptom, preques_infor,diag_list
#     else:
#         return final_answers, wait_symptom, arrive_symptom, preques_infor,diag_list
#
# def word_vect(sent):
#     # 分词结果输出
#     result = {}
#     # 获取关键词
#     result_key=[]
#     final_scores=[]
#     res=[]
#     chars,tags=lstm_predict.predict(sent)
#     key1=lstm_predict.match_key(chars,tags)#提取症状
#     if len(key1) != 0:#能提取到症状词，再提取症状修饰词这些
#         key2=extract_answerkey.ti_idf(sent)
#         key=key1+key2
#         result_key=list(set(key))#最终关键词
#
#         if "抑郁症" in result_key:  # 特殊情况处理(抑郁症匹配效果不好，转换为抑郁）
#             i = result_key.index("抑郁症")
#             result_key[i] = "抑郁"
#
#         result_key = list(set(result_key))
#         tran_key=(",".join(result_key))#关键词拼接去寻找相似症状
#
#         #获取相似症状
#         final_scores,res=sim_cilin.key_match_finalkey(tran_key)
#
#     # 获取句子正负情绪，主要用于是否输出关键词
#     sentiment_result = apiTest.sentiment(sent)
#
#     #获取程度词，时间词，频率词
#     other_result=extract_answerkey.match_otheranswer(sent)
#     # print("结果".center(50, "*"))
#     if sentiment_result == False:
#         sentiment_result = [2,0.5,0.5]
#     if sentiment_result[2]>0.9:#积极
#         if len(final_scores)>0:#如果没有匹配到相似症状，则没有必要显示关键词
#             result['keyword'] = result_key
#             # print("关键词：",result_key)
#         # print(("相似的症状的评分: " + str(final_scores)))
#         # print(("相似的症状: " + str(res)))
#         # print("程度词，时间词，频率词:",other_result)
#     # else:
#         # print(("相似的症状的评分: " + str(final_scores)))
#         # print(("相似的症状: " + str(res)))
#         # print("程度词，时间词，频率词:",other_result)
#     result['syms_score'] = final_scores
#     result['symptoms'] = res
#     result['other_words'] = other_result
#     # print("end".center(54, "-"))
#     return result

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run()