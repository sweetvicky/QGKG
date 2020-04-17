# 建立关系实体数据库

首先运行deal_data.py将数据插入到mongodb,
然后从mongodb导出json文件

然后build_kg根据json文件生成KG

# QAKG
基于知识图谱的问答+echarts展示图谱

环境：python3.6

首先运行build_kg将数据导入neo4j

然后运行build_graph.py以后
访问 http://127.0.0.1:5000/index.html 可以看到菜单

question.txt中给出了问题模板

main是单独的对话，也可以运行main

如果是对话的话，主要是qclasfier，qtransfer和qresult三个文件

build-kg的作用是导数据进入数据库，build-graph是生成一个页面包括对话和图谱展示，main是单纯的对话，就是在控制台输入对话

对问句的解析和查找数据库主要是qclasfier，qtransfer和qresult三个文件