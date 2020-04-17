import os
import re
import json
from py2neo import Graph,Node
import pandas as pd

class MedicalGraph:
    def __init__(self):
        # cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # self.disease_path = os.path.join(cur_dir, 'kgdata/Disease.json')
        # self.drug_path = os.path.join(cur_dir, 'kgdata/Drug.json')
        # self.symptom_path = os.path.join(cur_dir, 'kgdata/Symptom.json')
        self.g = Graph(
            host="127.0.0.1",  # neo4j 搭载服务器的ip地址，ifconfig可获取到
            http_port=7474,  # neo4j 服务器监听的端口号
            user="neo4j",  # 数据库user name，如果没有更改过，应该是neo4j
            password="123456")
        self.root_path = 'kgdata/'
        self.need_export = ['disease', 'sub_disease', 'up_symptom', 'down_symptom', \
                            'check', 'check_factor', 'treatment', 'up_drug', 'down_drug']

    def read_data(self):
        nodes_list = []
        edges_list = []
        lists = os.listdir(self.root_path)
        for filename in lists:
            file_path = self.root_path + filename
            type = filename.split('_')[0]
            if type == 'node':
                node_dict = {}
                data = pd.read_excel(file_path, encoding='utf8')
                node_dict['node_type'] = data.columns.values[0] # 后面可以考虑加其他的参数
                node_dict['name_list'] = sum(data.values.tolist(), [])
                nodes_list.append(node_dict)
                # 这里加一个导出文档
                # if node_dict['node_type'] in self.need_export:
                #     self.export_node(node_dict['node_type'], node_dict['name_list'])
            elif type == 'edge':
                edge_dict = {}
                data = pd.read_excel(file_path, encoding='utf8')
                edge_dict['start_type'] = data.columns.values[0]
                edge_dict['rela_type'] = data.loc[0,data.columns.values[1]]
                edge_dict['end_type'] = data.columns.values[2]
                edge_dict['rela_name'] = edge_dict['rela_type'] # 这个可能后面在做修改吧，现在先这样
                edge_dict['rela_pair'] = data[[edge_dict['start_type'],edge_dict['end_type']]].values.tolist()
                edges_list.append(edge_dict)
        return nodes_list, edges_list

    def build_graph(self,nodes_list, edges_list):
        for node_dict in nodes_list:
            self.creat_node(node_dict)
        for edge_dict in edges_list:
            start_node = edge_dict['start_type']
            end_node = edge_dict['end_type']
            rela_pair = edge_dict['rela_pair']
            rela_type = edge_dict['rela_type']
            rela_name = edge_dict['rela_name']
            self.creat_edge(start_node, end_node, rela_pair, rela_type, rela_name)


    def creat_node(self, node_dict):
        node_type = node_dict['node_type']
        name_list = node_dict['name_list']
        for name in name_list:
            node = Node(node_type, name=name)
            self.g.create(node)

    def creat_edge(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        # all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                # count += 1
                # print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    def export_node(self, name, nodelist):
        filestr = 'nodetxt/' + name + '.txt'
        file = open(filestr, 'w+')
        file.write('\n'.join(nodelist))
        file.close()


if __name__ == '__main__':
    handler = MedicalGraph()
    # handler.create_graph()

    nodes_list, edges_list = handler.read_data()
    handler.build_graph(nodes_list, edges_list)
    print('nihao')