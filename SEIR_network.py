# This is the SEIR_network model
import networkx as nx
import matplotlib.pyplot as plt
import random

node_attribute_list = ["state", "identity", "is_updated"]#is_updated refers to state change, not distance change
SI_rate = [0.8, 0.2]  # Suspected,Infectious
rv_rate = [0.7, 0.3]  # resident,visitor
network_parameter_list = ["se_rate", "se_distance", "ei_rate", "ir_rate", "nodes_num"]
valid_state = ["S", "E", "I", "R"]

class SEIR_network:
    def __init__(self, se_rate=0.2, se_distance=5, ei_rate=0.2, ir_rate=0.2, nodes_num=30):
        #initialize parameter
        self.graph = nx.Graph(name="region")
        self.se_rate = se_rate
        self.se_distance = se_distance
        self.ei_rate = ei_rate
        self.ir_rate = ir_rate
        self.rate_dict = {"se_rate": self.se_rate, "ei_rate": self.ei_rate, "ir_rate": self.ir_rate}
        self.nodes_num = nodes_num #initialize nodes_num
        self.actual_nodes_num = nodes_num #actual_nodes_num
        self.edge_list = []  # edge pair of (a b)
        self.remove_nodes_list = []

        self.resident_list = []
        self.visitor_list = []


        self.graph_nodes_initialize()
        self.graph_edges_random_graph()
        self.remove_no_degree_nodes()

        self.initial_pos = nx.spring_layout(self.graph)

        self.identity_register()




    def __str__(self):
        print("--------- Information Print Started ---------")
        print("SEIR Network Information:")
        print(self.rate_dict)
        print("se_distance", self.se_distance)
        print("nodes_num", self.nodes_num)
        print("actual nodes_num", self.actual_nodes_num)
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            print("Nodes id:",i)
            for j in node_attribute_list:
                print(j + ":", self.graph.nodes[i][j])
        print(self.edge_list)
        return "--------- Information Print Finished ---------"

    def graph_nodes_initialize(self):
        assert self.nodes_num >= 0
        # todo: use distribution instead of random
        for i in range(0, self.nodes_num):
            nodes_attribute = []
            rn = random.randint(0, 100) / 100
            if rn <= SI_rate[0]:
                nodes_attribute.append("S")
            else:
                nodes_attribute.append("I")
            rn = random.randint(0, 100) / 100
            if rn <= rv_rate[0]:
                nodes_attribute.append("resident")
            else:
                nodes_attribute.append("visitor")
            nodes_attribute.append(False)
            self.graph.add_node(i)
            for j in range(0, len(node_attribute_list)):
                self.graph.nodes[i][node_attribute_list[j]] = nodes_attribute[j]


    def graph_edges_random_graph(self):
        # random graph in Modelling Strong Control Measures for Epidemic Propagation With Networks—A COVID-19 Case Study
        total_edges = int(self.nodes_num * 4 / 2)  # mean degree equal to four
        for i in range(0, total_edges):
            # todo: make it uniform
            node_a = 0
            node_b = 0
            # avoid self loop
            while node_a == node_b:
                node_a = random.randint(0, self.nodes_num-1)
                node_b = random.randint(0, self.nodes_num-1)
                # avoid multiple edges
                if (node_a, node_b) in self.edge_list or (node_b, node_a) in self.edge_list:
                    continue
            self.edge_list.append((node_a, node_b))
            self.graph.add_edge(node_a, node_b, distance=random.uniform(0, self.se_distance))#todo: have a complex one

    def remove_no_degree_nodes(self):
        for i in range(0, self.nodes_num):
            if self.graph.degree[i] == 0:
                print("Remove node: " + str(i))
                self.remove_nodes_list.append(i)
                self.graph.remove_node(i)
                self.actual_nodes_num -= 1

    def identity_register(self):
        #initialize the resident and visitor list for plot
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            identity = self.graph.nodes[i]["identity"]
            if identity == "resident":
                self.resident_list.append(i)
            else:
                self.visitor_list.append(i)

        assert len(self.resident_list)+len(self.visitor_list) == self.actual_nodes_num

    def get_state_list(self,state):
        assert state in valid_state
        res = [i for i in self.graph.nodes() if i not in self.remove_nodes_list and self.graph.nodes[i].get("state") == state]
        return res

    def graph_draw(self, verbose_level=0,epochs=0):
        G = self.graph
        pos = self.initial_pos
        if verbose_level == 0:
            nx.draw(G,with_labels=True)
            plt.show()
        elif verbose_level == -1:
            nx.draw_networkx_edges(G,pos=nx.kamada_kawai_layout(G))
            plt.show()
        elif verbose_level == 1:
            #draw nodes blue:yellow:red:green
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("S"),node_color="#1f78b4")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("E"),node_color="#ffff33")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("I"), node_color="#ff0000")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("R"), node_color="#00ff00")
            #draw edges todo:highlight distance < se_distance
            nx.draw_networkx_edges(G, pos=pos)
            #draw labels
            resident_dict={}
            visitor_dict={}
            for i in self.resident_list:
                resident_dict.update({i: "R"+str(i)})
            for i in self.visitor_list:
                visitor_dict.update({i: "V"+str(i)})
            nx.draw_networkx_labels(G, pos=pos,labels=resident_dict,font_color="#190033",font_size=8)
            nx.draw_networkx_labels(G, pos=pos, labels=visitor_dict, font_color="#000000",font_size=8)
            #plt.show()
    def graph_move(self):
        print("todo!")
        #first setup all nodes as not updated in this round
        for i in range(0, self.nodes_num):
            nx.set_node_attributes(self.graph,values=False,name="is_updated")
        #todo:first is the change of state judgement
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            # has been update, no need for update state
            if not self.graph.nodes(data=True)[i]["is_updated"]:

                if self.graph.nodes(data=True)[i]["state"] == "S":
                    # S state, check wether neighbors have I
                    infectious_neighbors = [n for n in self.graph.neighbors(i) if self.graph.nodes[n].get("state") == "I"]
                    infectious_distance = [self.graph.get_edge_data(i, j).get("distance") for j in infectious_neighbors]
                    if len(infectious_neighbors) > 0:
                        for j in infectious_distance:
                            if j < self.se_distance:
                                rn=random.randint(0,100)/100
                                if rn < self.se_rate:
                                    self.graph.nodes(data=True)[i]["is_updated"]=True
                                    self.graph.nodes(data=True)[i]["state"]="E"
                                    print("nodes "+str(i)+" get exposed!")

                if self.graph.nodes(data=True)[i]["state"] == "E":
                    # E state, check whether will go to I
                    rn=random.randint(0,100)/100
                    if rn < self.ei_rate:
                        self.graph.nodes(data=True)[i]["is_updated"]=True
                        self.graph.nodes(data=True)[i]["state"]="I"
                        print("Exposed node "+str(i)+" get infectious!")

                if self.graph.nodes(data=True)[i]["state"] == "I":
                    # I state, check whether will go to R
                    # todo: I to check nearby E to save
                    rn=random.randint(0,100)/100
                    if rn < self.ir_rate:
                        self.graph.nodes(data=True)[i]["is_updated"]=True
                        self.graph.nodes(data=True)[i]["state"]="R"
                        print("Infectious node "+str(i)+" get recovered!")

                #todo: recover node remove






        #todo:within each round, each node choose to random get close to or get away from its neighbours



G = nx.Graph()
G.add_node(1)
'''
for i in node_attribute_list:
    G.nodes[1][i]="E"
print(G.nodes[1])
for node in G.nodes:
    print()
nx.draw(G,with_labels=True)
'''
# plt.show()
a = SEIR_network(nodes_num=30)

#print(a)
for num_epochs in range(0,20):
    plt.clf()
    save_fn = './Net_epoch_{:d}'.format(num_epochs) + '.png'
    a.graph_draw(verbose_level=1,epochs=num_epochs)
    plt.savefig(save_fn)
    a.graph_move()
#print(a)
#print(a.get_state_list("I"))