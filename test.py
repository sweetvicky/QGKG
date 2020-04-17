from py2neo import Graph


g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456")
datas = ['睡眠过多']
# datas = ['睡眠过多']

sql = ["MATCH (m:down_symptom)-[r:sub_sub_symptom]->(n:down2_symptom) where n.name = '{0}' return m.name".format(i) for i in datas]
ress = g.run(sql[0]).data()
keyword = list(set([i['m.name'] for i in ress]))
print(keyword)