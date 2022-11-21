import SEIR_network
import matplotlib.pyplot as plt

# system variables
valid_mode = ["statistical", "graph"]


# main driver
class driver:
    def __init__(self, mode="graph", epochs=20, network_parameters=None):
        assert mode in valid_mode
        self.mode = mode
        self.epochs = epochs
        if network_parameters is None:
            self.network = SEIR_network.SEIR_network()
        else:
            se_rate, se_distance, ei_rate, ir_rate, nodes_num = network_parameters
            self.network = SEIR_network.SEIR_network(se_rate, se_distance, ei_rate, ir_rate, nodes_num)

    def graph_visualize(self, num_epochs, is_save=True):
        assert self.mode == "graph"
        if is_save:
            plt.clf()
            save_fn = './result/Net_epoch_{:d}'.format(num_epochs) + '.png'
            self.network.graph_draw(verbose_level=1)
            plt.savefig(save_fn)
        else:
            plt.clf()
            self.network.graph_draw(verbose_level=1)
            plt.show()
            # self.network.graph_move()

    def graph_main(self):
        for num_epochs in range(0, self.epochs):
            self.graph_visualize(num_epochs)
            self.network.graph_move()

    
    def statistical_main(self):
        print("todo")

    def driver_main(self):
        if self.mode == "graph":
            self.graph_main()
        else:
            self.statistical_main()


a = driver()
a.driver_main()
