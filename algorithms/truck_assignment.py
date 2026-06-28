from entities.node import Depot
from entities.order import Order
from entities.node import Node
from datetime import timedelta


def truck_routes_for_depot(depot: Depot, order_list: list[Order], shortest_paths: dict):
    ALPHA = 10  # lateness penalty weight
    unassigned_orders = set(order_list)

    # largest trucks first
    trucks = sorted(depot.truck_list, key=lambda t: t.capacity, reverse=True)

    def get_best_order(current_node: Node, current_time, remaining_capacity: int) -> Order | None:
        best_order = None
        best_cost = float("inf")

        for order in unassigned_orders:
            # capacity feasibility
            if order.required_amount > remaining_capacity:
                continue

            travel_minutes = shortest_paths[current_node][order.recipient_location]["length"]

            arrival_time = (
                current_time
                + timedelta(minutes=travel_minutes)
            )

            lateness_minutes = max(
                0,
                (arrival_time - order.deadline).total_seconds() / 60
            )

            cost = (
                travel_minutes
                + ALPHA * lateness_minutes
            )

            if cost < best_cost:
                best_cost = cost
                best_order = order

        return best_order

    # Build one route per truck
    for truck in trucks:
        if not unassigned_orders:
            break

        route = [depot]
        current_node = depot
        current_time = truck.available_from
        remaining_capacity = truck.capacity

        while True:
            best_order = get_best_order(
                current_node,
                current_time,
                remaining_capacity
            )

            if best_order is None:
                break

            # travel to order
            travel_minutes = shortest_paths[current_node][best_order.recipient_location]["length"]
            current_time += timedelta(minutes=travel_minutes)
            truck.available_from = current_time

            route.append(best_order.recipient_location)
            remaining_capacity -= best_order.required_amount
            current_node = best_order.recipient_location
            unassigned_orders.remove(best_order)

        route.append(depot)
        truck.routes.append(route)

    # Any remaining orders?
    if unassigned_orders:
        print(
            f"{len(unassigned_orders)} orders "
            "could not be assigned."
        )

        return {
            "assigned": list(set(order_list) - unassigned_orders),
            "unassigned": list(unassigned_orders)
        }

    return {
        "assigned": order_list,
        "unassigned": []
    }


def truck_assignment(depot_list: list[Depot], shortest_paths: dict):
    results = {}

    for depot in depot_list:
        results[depot] = truck_routes_for_depot(depot, depot.order_list, shortest_paths)

    for depot, result in results.items():
        print(f"For depot {depot.node_id}: {result}")
        for truck in depot.truck_list:
            print(f"Truck {truck.capacity}: {[[node.node_id for node in route] for route in truck.routes]}")

    return results
