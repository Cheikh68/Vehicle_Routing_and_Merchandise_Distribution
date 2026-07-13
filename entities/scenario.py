from data.data_loader import load_scenario, get_graph, get_depot_list, get_destination_list, get_order_list, \
    get_shortest_path_graph


class Scenario:
    ALPHA: int
    BETA: int
    GAMMA: int

    def __init__(self, filename, alpha, beta, gamma):
        self.ALPHA = alpha
        self.BETA = beta
        self.GAMMA = gamma

        data = load_scenario(filename)

        self.graph, self.node_lookup = get_graph(data)

        self.depots = get_depot_list(self.graph)

        self.destinations = get_destination_list(self.graph)

        self.orders = get_order_list(
            data,
            self.node_lookup
        )

        self.shortest_paths = get_shortest_path_graph(
            self.graph
        )
