# This is the SEIR_network model
import networkx as nx
import matplotlib.pyplot as plt
import random
node_attribute_list=["state" , "identity"]
SI_rate=[0.8,0.2]#Suspected,Infectious
rv_rate=[0.7,0.3]#resident,visitor
network_parameter_list=["se_rate","se_distance","ei_rate","ir_rate","nodes_num"]
class SEIR_network:
    def __init__(self,se_rate=0.2,se_distance=5,ei_rate=0.2,ir_rate=0.2,nodes_num=10):
        self.graph = nx.Graph(name="region")
        self.se_rate=se_rate
        self.se_distance=se_distance
        self.ei_rate=ei_rate
        self.ir_rate=ir_rate
        self.rate_dict={"se_rate":self.se_rate, "ei_rate":self.ei_rate, "ir_rate":self.ir_rate}
        self.nodes_num=nodes_num
        self.graph_nodes_initialize()

    def __str__(self):
        print("--------- Information Print Started ---------")
        print("SEIR Network Information:")
        print(self.rate_dict)
        print("se_distance",self.se_distance)
        print("nodes_num", self.nodes_num)
        for i in range(0,self.nodes_num):
            for j in node_attribute_list:
                print(j+":",self.graph.nodes[i][j])
        return "--------- Information Print Finished ---------"

    def graph_nodes_initialize(self):
        assert self.nodes_num >= 0
        #todo: use distribution instead of random
        for i in range(0,self.nodes_num):
            nodes_attribute=[]
            rn=random.randint(0,100)/100
            if rn <= SI_rate[0]:
                nodes_attribute.append("S")
            else:
                nodes_attribute.append("I")
            if rn <= rv_rate[0]:
                nodes_attribute.append("resident")
            else:
                nodes_attribute.append("visitor")
            self.graph.add_node(i)
            for j in range(0,len(node_attribute_list)):
                self.graph.nodes[i][node_attribute_list[j]]=nodes_attribute[j]









G=nx.Graph()
G.add_node(1)
'''
for i in node_attribute_list:
    G.nodes[1][i]="E"
print(G.nodes[1])
for node in G.nodes:
    print()
nx.draw(G,with_labels=True)
'''
#plt.show()
a=SEIR_network()
print(a)