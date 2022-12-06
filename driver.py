import SEIR_network
import matplotlib.pyplot as plt
import os
import numpy as np

# system variables
valid_mode = ["statistical", "graph"]


# main driver
class driver:
    def __init__(self, mode="graph", epochs=20, network_parameters=None):
        assert mode in valid_mode
        self.mode = mode
        self.epochs = epochs
        if network_parameters is None:
            if mode == "graph":
                self.network = SEIR_network.SEIR_network()
                self.event_start_day=0
                self.event_days=6
            else:
                self.network = SEIR_network.SEIR_network(is_visualize=False)
                self.event_start_day = 0
                self.event_days = 6
        else:
            se_rate, se_distance, ei_rate, ir_rate, nodes_num,event_start_day,\
            event_days = network_parameters
            self.event_start_day = event_start_day
            self.event_days = event_days
            if mode == "graph":
                self.network = SEIR_network.SEIR_network(se_rate, se_distance, ei_rate, ir_rate, nodes_num,
                                                         event_start_day, event_days)
            else:
                self.network = SEIR_network.SEIR_network(se_rate, se_distance, ei_rate, ir_rate, nodes_num,
                                                         event_start_day, event_days,is_visualize=False)

    def graph_visualize(self, num_epochs, is_save=True):
        assert self.mode == "graph"
        if is_save:
            plt.clf()
            save_fn = './result/Net_epoch_{:d}'.format(num_epochs) + '.png'
            self.network.graph_draw(current_day=num_epochs,verbose_level=1)
            plt.savefig(save_fn)
        else:
            plt.clf()
            self.network.graph_draw(current_day=num_epochs,verbose_level=1)
            plt.show()
            # self.network.graph_move()

    def graph_main(self):
        for num_epochs in range(0, self.epochs):
            self.graph_visualize(num_epochs)
            self.network.graph_move(num_epochs)

    def plot_number(self, s_num_list, e_num_list, i_num_list, r_num_list,event_start_day,event_days, save=False, show=False,
                    save_dir='results_s/'):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.epochs)

        ylim = self.network.nodes_num
        ylim_low = 0
        ax.set_ylim(ylim_low, ylim)
        plt.xlabel('Days')
        plt.ylabel('People')
        plt.plot(s_num_list, label='Suspected people number', color="#1f78b4")
        plt.plot(e_num_list, label='Exposed people number', color="#ffff33")
        plt.plot(i_num_list, label='Infectious people number', color="#ff0000")
        plt.plot(r_num_list, label='Recovered people number', color="#00ff00")
        plt.legend()
        ax.vlines([event_start_day, event_start_day+event_days], ylim_low, ylim,
                  linestyles='dashed', colors=['red','b'])
        plt.plot(event_start_day + event_days, ls="dashed", color="#000000")

        # save figure
        if save:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            save_fn = save_dir + 'Statistical_Result_{:d}'.format(self.epochs) + '.png'
            plt.savefig(save_fn)

        if show:
            plt.show()
        else:
            plt.close()

    def statistical_main(self):
        s_num_list = []
        e_num_list = []
        i_num_list = []
        r_num_list = []
        for i in range(0, self.epochs):
            print("epochs: {:d}/{:d}".format(i, self.epochs))
            s_num_list.append(self.network.get_state_number("S"))
            e_num_list.append(self.network.get_state_number("E"))
            i_num_list.append(self.network.get_state_number("I"))
            r_num_list.append(self.network.get_state_number("R"))
            self.network.graph_move(i)
        self.plot_number(s_num_list=s_num_list, e_num_list=e_num_list, i_num_list=i_num_list,
                         r_num_list=r_num_list,event_start_day=self.event_start_day,
                         event_days=self.event_days ,save=True)

    def driver_main(self):
        if self.mode == "graph":
            self.graph_main()
        else:
            self.statistical_main()

# "se_rate", "se_distance", "ei_rate", "ir_rate", "nodes_num","event_start_day",
#                  "event_days"

network_para_s=[0.8, 3, 0.5, 0.15, 500, 2, 9]
a = driver(mode="statistical",epochs=35,network_parameters=network_para_s)
a.driver_main()
