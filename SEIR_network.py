# This is the SEIR_network model
import networkx as nx
import matplotlib.pyplot as plt
node_attribute_list=["state" , "identity"]
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
    def __str__(self):
        print("SEIR Network Information:")
        print(self.rate_dict)
        print("se_distance",self.se_distance)
        print("nodes_num", self.nodes_num)









G=nx.Graph()
G.add_node(1)
for i in node_attribute_list:
    G.nodes[1][i]="E"
print(G.nodes[1])
for node in G.nodes:
    print()
nx.draw(G,with_labels=True)
plt.show()
a=SEIR_network()
print(a)