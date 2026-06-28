from dataclasses import dataclass, field
from entities.truck import Truck
from entities.order import Order


@dataclass
class Node:
    node_id: int

    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.node_id


@dataclass(eq=False)
class Depot(Node):
    available_stock: int
    truck_list: list[Truck]

    order_list: list[Order] = field(init=False)

    def __post_init__(self):
        self.order_list = []
