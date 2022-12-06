# This is the SEIR_network model
import networkx as nx
import matplotlib.pyplot as plt
import random

debug_mode = False
event_mode = True
node_attribute_list = ["state", "identity", "is_updated"]  # is_updated refers to state change, not distance change
SI_rate = [0.8, 0.2]  # Suspected,Infectious
rv_rate = [0.95, 0.05] if not event_mode else [0.6, 0.4]  # resident,visitor
network_parameter_list = ["se_rate", "se_distance", "ei_rate", "ir_rate", "nodes_num"]
valid_state = ["S", "E", "I", "R"]


class SEIR_network:
    def __init__(self, se_rate=0.2, se_distance=5, ei_rate=0.2, ir_rate=0.2, nodes_num=30, event_start_day=0,
                 event_days=6, is_visualize=True):
        # initialize parameter
        self.graph = nx.Graph(name="region")
        self.se_rate = se_rate
        self.se_distance = se_distance
        self.ei_rate = ei_rate
        self.ir_rate = ir_rate
        self.rate_dict = {"se_rate": self.se_rate, "ei_rate": self.ei_rate, "ir_rate": self.ir_rate}
        self.nodes_num = nodes_num  # initialize nodes_num
        self.actual_nodes_num = nodes_num  # actual_nodes_num
        self.event_start_day = event_start_day
        self.event_days = event_days
        self.edge_list = []  # edge pair of (a b)
        self.remove_nodes_list = []

        self.resident_list = []
        self.visitor_list = []

        self.graph_nodes_initialize()
        self.graph_edges_random_graph()
        self.remove_no_degree_nodes()
        self.graph_nodes_identity_rearrange()
        if is_visualize:
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
            print("Nodes id:", i)
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

            # identity will be decided on centrality
            nodes_attribute.append("undecided")

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
                node_a = random.randint(0, self.nodes_num - 1)
                node_b = random.randint(0, self.nodes_num - 1)
                # avoid multiple edges
                if (node_a, node_b) in self.edge_list or (node_b, node_a) in self.edge_list:
                    continue
            self.edge_list.append((node_a, node_b))
            self.graph.add_edge(node_a, node_b, distance=random.uniform(self.se_distance,
                                                                        1.5 * self.se_distance))  # todo: have a complex one

    def graph_nodes_identity_rearrange(self):
        central_order_list = sorted(nx.degree_centrality(self.graph).items(), key=lambda x: x[1])
        resident_count = 0
        vistor_count = 0
        vistor_number = int(rv_rate[1] * self.actual_nodes_num)
        for i in range(0, len(central_order_list)):
            node_index = central_order_list[i][0]
            rn = random.randint(0, 100) / 100
            if vistor_count < int(vistor_number/2):
                resident_rate = rv_rate[0] * (self.actual_nodes_num - i) / self.actual_nodes_num * (
                            vistor_number + vistor_count) / vistor_number
            else:
                resident_rate = rv_rate[0] * (self.actual_nodes_num - i) / self.actual_nodes_num
            # the lower centrality, the higher possibility it will be vistor
            if rn <= resident_rate:
                self.graph.nodes[node_index]["identity"] = "visitor"
                vistor_count += 1
            else:
                self.graph.nodes[node_index]["identity"] = "resident"
                resident_count += 1

        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            assert self.graph.nodes[i]["identity"] in ["visitor", "resident"]
        print(resident_count, vistor_count,vistor_number)

    def remove_no_degree_nodes(self):
        for i in range(0, self.nodes_num):
            if self.graph.degree[i] == 0:
                print("Remove node: " + str(i))
                self.remove_nodes_list.append(i)
                self.graph.remove_node(i)
                self.actual_nodes_num -= 1

    def identity_register(self):
        # initialize the resident and visitor list for plot
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            identity = self.graph.nodes[i]["identity"]
            if identity == "resident":
                self.resident_list.append(i)
            else:
                self.visitor_list.append(i)

        assert len(self.resident_list) + len(self.visitor_list) == self.actual_nodes_num

    def get_state_number(self, state):
        assert state in valid_state
        return len(self.get_state_list(state))

    def get_state_list(self, state):
        assert state in valid_state
        res = [i for i in self.graph.nodes() if
               i not in self.remove_nodes_list and self.graph.nodes[i].get("state") == state]
        return res

    def get_edge_list_distance(self, is_larger):

        edge_list = [i for i in self.graph.edges(data=True)]
        if is_larger:
            res = [i for i in edge_list if i[2].get("distance") > self.se_distance]
        else:
            res = [i for i in edge_list if i[2].get("distance") <= self.se_distance]
        return res

    def graph_draw(self, current_day, verbose_level=0):
        G = self.graph
        pos = self.initial_pos
        if verbose_level == 0:
            nx.draw(G, with_labels=True)
            plt.show()
        elif verbose_level == -1:
            nx.draw_networkx_edges(G, pos=nx.kamada_kawai_layout(G))
            plt.show()
        elif verbose_level == 1:
            # draw nodes blue:yellow:red:green
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("S"), node_color="#1f78b4")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("E"), node_color="#ffff33")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("I"), node_color="#ff0000")
            nx.draw_networkx_nodes(G, pos=pos, nodelist=self.get_state_list("R"), node_color="#00ff00")
            # draw edges todo:highlight distance < se_distance
            nx.draw_networkx_edges(G, pos=pos, edgelist=self.get_edge_list_distance(is_larger=True),
                                   edge_color="#000000")
            nx.draw_networkx_edges(G, pos=pos, edgelist=self.get_edge_list_distance(is_larger=False),
                                   edge_color="#cc0000")
            # draw labels
            resident_dict = {}
            visitor_dict = {}
            for i in self.resident_list:
                resident_dict.update({i: "R" + str(i)})
            for i in self.visitor_list:
                visitor_dict.update({i: "V" + str(i)})
            nx.draw_networkx_labels(G, pos=pos, labels=resident_dict, font_color="#190033", font_size=8)
            nx.draw_networkx_labels(G, pos=pos, labels=visitor_dict, font_color="#000000", font_size=8)
            # plt.show()
            if current_day < self.event_start_day:
                plt.title('Day {:d} '.format(current_day) + '{:d} Day(s) to event'.format(self.event_start_day-current_day))
            elif self.event_start_day <= current_day <= self.event_start_day + self.event_days:
                plt.title(
                    'Day {:d} '.format(current_day) + 'Event Day {:d}'.format(current_day - self.event_start_day + 1))
            else:
                plt.title(
                    'Day {:d} '.format(current_day) + 'After Event')

    def graph_move(self, current_day):

        # setup all nodes as not updated in this round
        for i in range(0, self.nodes_num):
            nx.set_node_attributes(self.graph, values=False, name="is_updated")
        # the change of state judgement
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            # has been update, no need for update state
            if not self.graph.nodes(data=True)[i]["is_updated"]:

                if self.graph.nodes(data=True)[i]["state"] == "S":
                    # S state, check wether neighbors have I
                    infectious_neighbors = [n for n in self.graph.neighbors(i) if
                                            self.graph.nodes[n].get("state") == "I"]
                    infectious_distance = [self.graph.get_edge_data(i, j).get("distance") for j in infectious_neighbors]
                    if len(infectious_neighbors) > 0:
                        for j in infectious_distance:
                            if j < self.se_distance:
                                rn = random.randint(0, 100) / 100
                                if rn < self.se_rate:
                                    self.graph.nodes(data=True)[i]["is_updated"] = True
                                    self.graph.nodes(data=True)[i]["state"] = "E"
                                    if debug_mode:
                                        print("nodes " + str(i) + " get exposed!")
                                    break

                if self.graph.nodes(data=True)[i]["state"] == "E":
                    # E state, check whether will go to I
                    rn = random.randint(0, 100) / 100
                    if rn < self.ei_rate:
                        self.graph.nodes(data=True)[i]["is_updated"] = True
                        self.graph.nodes(data=True)[i]["state"] = "I"
                        if debug_mode:
                            print("Exposed node " + str(i) + " get infectious!")

                if self.graph.nodes(data=True)[i]["state"] == "I":
                    # I state, check whether will go to R
                    # todo: I to check nearby E to save
                    exposed_neighbors = [n for n in self.graph.neighbors(i) if
                                         self.graph.nodes[n].get("state") == "E"]
                    exposed_distance = [self.graph.get_edge_data(i, j).get("distance") for j in exposed_neighbors]
                    if len(exposed_neighbors) > 0:
                        for j, k in list(zip(exposed_distance, exposed_neighbors)):
                            if j < self.se_distance and not self.graph.nodes(data=True)[k]["is_updated"]:
                                rn = random.randint(0, 100) / 100
                                if rn < self.se_rate:
                                    self.graph.nodes(data=True)[k]["is_updated"] = True
                                    self.graph.nodes(data=True)[k]["state"] = "E"
                                    if debug_mode:
                                        print("nodes " + str(k) + " get exposed due to closed to infectious node" + str(
                                            i) + "!")

                    rn = random.randint(0, 100) / 100
                    if rn < self.ir_rate:
                        self.graph.nodes(data=True)[i]["is_updated"] = True
                        self.graph.nodes(data=True)[i]["state"] = "R"
                        if debug_mode:
                            print("Infectious node " + str(i) + " get recovered!")

                # todo: recover node remove
                if self.graph.nodes(data=True)[i]["state"] == "R":
                    j = 1

        # within each round, each node choose to random get close to or get away from its neighbours
        for i in range(0, self.nodes_num):
            if i in self.remove_nodes_list:
                continue
            self.node_move(i, current_day)

    '''
    Idea of node move
    If not in event mode:
    both residents and visitors will keep wandering (50% get close to each other and 50% get away from each
    other if in S and E, in I, they will a high rate to get away from each other. For R, just do nothing, I
    treat R nodes as meaningless nodes in this mode.
    In event mode:
    residents:
    before event starts: like not in event mode
    event starts --- event ends: likely to get gather (distance --), I nodes have a lower rate to get away
    after: like not in event mode
    visitor:
    before event starts: get close to neighbours unless in I (R also will get close to neighbours!)
    event starts --- event ends: likely to get gather (distance --), 
    I nodes have a lower rate to get away (R also will get close to neighbours!)
    after: get away (also applied to R)
    
    
    '''
    def node_move(self, node, current_day):

        if (debug_mode):
            print("Current calling: node_move")
            print("Current at Node " + str(node))
            print("Current Node state: " + self.graph.nodes(data=True)[node]["state"])
        neighbors = [n for n in self.graph.neighbors(node)]
        distance = [self.graph.get_edge_data(node, j).get("distance") for j in neighbors]

        state = self.graph.nodes(data=True)[node]["state"]

        if state == "R":
            if not event_mode:
                return  # recovered node will do thing if no event
            else:
                # in event mode, visitors will go close if event hasn't finished else leave
                if self.graph.nodes(data=True)[node]["identity"] == "visitor":
                    if current_day <= self.event_start_day + self.event_days:
                        for neighbor, dis in list(zip(neighbors, distance)):
                            rn_distance = random.uniform(0, 2 * dis / 3)
                            self.graph[node][neighbor]["distance"] = dis - rn_distance
                    else:
                        for neighbor, dis in list(zip(neighbors, distance)):
                            rn_distance = random.uniform(2 * self.se_distance, 3 * self.se_distance)
                            self.graph[node][neighbor]["distance"] = dis + rn_distance
                # for residents, they will do nothing.




        # suspectible and exposed node will random choose to get close to or get away from neighbours
        elif state == "S" or "E":
            if current_day < self.event_start_day and event_mode:
                # before events begin, all visitor nodes will try to gather
                if self.graph.nodes(data=True)[node]["identity"] == "visitor":
                    for neighbor, dis in list(zip(neighbors, distance)):
                        rn_distance = random.uniform(0, 2 * dis / 3)
                        self.graph[node][neighbor]["distance"] = dis - rn_distance
                else:  # residents will behave as normal
                    for neighbor, dis in list(zip(neighbors, distance)):
                        rn1 = random.uniform(0, 1)  # get close to or get away
                        if rn1 <= 0.5:  # get close to
                            rn_distance = random.uniform(0, dis / 2)
                            self.graph[node][neighbor]["distance"] = dis - rn_distance
                        else:
                            rn_distance = random.uniform(0, dis / 2)
                            self.graph[node][neighbor]["distance"] = dis + rn_distance
            elif event_mode and self.event_start_day <= current_day <= self.event_days + self.event_start_day:
                # events begin, all nodes will have a high tendency to gather
                for neighbor, dis in list(zip(neighbors, distance)):
                    if debug_mode:
                        print("old distance to Node " + str(neighbor) + ": " + str(
                            self.graph.get_edge_data(node, neighbor)))
                    rn1 = random.uniform(0, 1)  # get close to or get away
                    close_tendency = 0.8
                    if rn1 <= close_tendency:  # get close to
                        rn_distance = random.uniform(0, 2 * dis / 3)
                        self.graph[node][neighbor]["distance"] = dis - rn_distance
                    else:
                        rn_distance = random.uniform(0, dis / 2)
                        self.graph[node][neighbor]["distance"] = dis + rn_distance
                    if debug_mode:
                        print("new distance to Node " + str(neighbor) + ": " + str(
                            self.graph.get_edge_data(node, neighbor)))
            else:
                # events ends, vistors will try to leave
                if self.graph.nodes(data=True)[node]["identity"] == "visitor":
                    for neighbor, dis in list(zip(neighbors, distance)):
                        rn_distance = random.uniform(0, dis / 2)
                        self.graph[node][neighbor]["distance"] = dis + rn_distance
                else:  # residents will behave as normal
                    for neighbor, dis in list(zip(neighbors, distance)):
                        rn1 = random.uniform(0, 1)  # get close to or get away
                        if rn1 <= 0.5:  # get close to
                            rn_distance = random.uniform(0, dis / 2)
                            self.graph[node][neighbor]["distance"] = dis - rn_distance
                        else:
                            rn_distance = random.uniform(0, dis / 2)
                            self.graph[node][neighbor]["distance"] = dis + rn_distance



        # infectious node will try to get away from neighbours at most of time but rarely get close to
        # this rate is higher during event for vistors
        else:
            assert state == "I"
            for neighbor, dis in list(zip(neighbors, distance)):
                if debug_mode:
                    print("old distance: " + str(self.graph.get_edge_data(node, neighbor)))
                is_danger = event_mode and self.graph.nodes(data=True)[node]["identity"] == "visitor" \
                            and self.event_start_day <= current_day <= self.event_days + self.event_start_day
                close_tendency = 0.35 if is_danger else 0.1
                rn1 = random.uniform(0, 1)  # get close to or get away
                if rn1 <= close_tendency:  # get close to
                    rn_distance = random.uniform(0, dis)
                    self.graph[node][neighbor]["distance"] = dis - rn_distance
                else:
                    rn_distance = random.uniform(0, dis)
                    self.graph[node][neighbor]["distance"] = dis + rn_distance
                if debug_mode:
                    print("new distance: " + str(self.graph.get_edge_data(node, neighbor)))


'''
for i in node_attribute_list:
    G.nodes[1][i]="E"
print(G.nodes[1])
for node in G.nodes:
    print()
nx.draw(G,with_labels=True)

# plt.show()
a = SEIR_network(nodes_num=50)

#print(a)
for num_epochs in range(0,20):
    plt.clf()
    save_fn = './result/Net_epoch_{:d}'.format(num_epochs) + '.png'
    a.graph_draw(verbose_level=1)
    plt.savefig(save_fn)
    a.graph_move()
#print(a)
#print(a.get_state_list("I"))
'''
