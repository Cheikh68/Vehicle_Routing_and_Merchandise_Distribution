import networkx as nx
from entities.node import Node, Depot
from entities.order import Order
from entities.truck import Truck
from datetime import datetime
import json


def load_scenario(filename: str):
    with open(filename, "r") as f:
        return json.load(f)


def get_graph(scenario):
    graph = nx.Graph()
    node_lookup = {}

    # Create depots
    for depot_data in scenario["depots"]:
        trucks = []

        for truck_data in depot_data["trucks"]:
            truck = Truck(truck_data["capacity"])
            trucks.append(truck)

        depot = Depot(
            depot_data["id"],
            depot_data["stock"],
            trucks
        )

        for truck in trucks:
            truck.current_location = depot

        node_lookup[depot.node_id] = depot

    # Create normal nodes
    for node_data in scenario["nodes"]:
        node = Node(node_data["id"])
        node_lookup[node.node_id] = node

    # Create edges
    for edge in scenario["edges"]:
        graph.add_edge(
            node_lookup[edge["from"]],
            node_lookup[edge["to"]],
            time_in_minutes=edge["time"]
        )

    return graph, node_lookup


def get_depot_list(graph):
    return [
        node
        for node in graph.nodes
        if isinstance(node, Depot)
    ]


def get_destination_list(graph):
    return [
        node
        for node in graph.nodes
        if isinstance(node, Node)
        and not isinstance(node, Depot)
    ]


def get_order_list(scenario, node_lookup):
    orders = []

    for order_data in scenario["orders"]:
        orders.append(
            Order(
                order_data["id"],
                order_data["amount"],
                node_lookup[order_data["destination"]],
                datetime.fromisoformat(order_data["deadline"])
            )
        )

    return orders


def get_shortest_path_graph(graph):
    shortest_paths = {}

    for source in graph:
        paths = nx.single_source_dijkstra_path(
            graph,
            source,
            weight="time_in_minutes"
        )

        lengths = nx.single_source_dijkstra_path_length(
            graph,
            source,
            weight="time_in_minutes"
        )

        shortest_paths[source] = {
            target: {
                "path": paths[target],
                "length": lengths[target]
            }
            for target in paths
            if target != source
        }

    return shortest_paths
