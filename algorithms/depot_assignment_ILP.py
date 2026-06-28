import pulp
from entities.node import Node, Depot
from entities.order import Order


def assign_order_to_depot(depot_list: list[Depot], shortest_paths: dict[Node, dict[Node, dict[str, list[Node] | float]]]
                          , order_list: list[Order]):
    model = pulp.LpProblem("JobAssignment", pulp.LpMinimize)

    # VARIABLES (tuple-key style)
    x = pulp.LpVariable.dicts(
        "assign",
        ((o, d) for o in order_list for d in depot_list),
        cat="Binary"
    )

    # OBJECTIVE
    model += pulp.lpSum(
        shortest_paths[d][o.recipient_location]["length"] * x[o, d]
        for o in order_list
        for d in depot_list
    )

    # Each order assigned exactly one depot
    for o in order_list:
        model += pulp.lpSum(x[o, d] for d in depot_list) == 1

    # Depot capacity constraint
    for d in depot_list:
        model += pulp.lpSum(
            o.required_amount * x[o, d]
            for o in order_list
        ) <= d.available_stock

    status = model.solve()

    print("Status:", pulp.LpStatus[status])
    for o in order_list:
        for d in depot_list:
            if pulp.value(x[o, d]) > 0.5:
                print(f"Order {o.order_id} assigned to Depot {d.node_id}")
                d.order_list.append(o)

    return x
