from datetime import timedelta
from entities.route import Route


def truck_routes_for_depot(depot, order_list, shortest_paths):
    ALPHA = 10
    unassigned_orders = set(order_list)

    trucks = sorted(
        depot.truck_list,
        key=lambda t: t.capacity,
        reverse=True
    )

    def get_best_order(current_node, current_time, remaining_capacity):
        best_order = None
        best_cost = float("inf")

        for order in unassigned_orders:
            if order.required_amount > remaining_capacity:
                continue

            travel = shortest_paths[
                current_node
            ][
                order.recipient_location
            ]["length"]

            arrival = current_time + timedelta(minutes=travel)

            lateness = max(
                0,
                (arrival - order.deadline).total_seconds()/60
            )

            cost = travel + ALPHA * lateness

            if cost < best_cost:
                best_cost = cost
                best_order = order

        return best_order

    for truck in trucks:
        if not unassigned_orders:
            break

        start_time = truck.available_from
        current_node = depot
        current_time = start_time
        remaining_capacity = truck.capacity

        route_orders = []

        while True:
            order = get_best_order(
                current_node,
                current_time,
                remaining_capacity
            )

            if order is None:
                break

            travel = shortest_paths[
                current_node
            ][
                order.recipient_location
            ]["length"]

            current_time += timedelta(minutes=travel)
            remaining_capacity -= order.required_amount
            current_node = order.recipient_location
            route_orders.append(order)
            unassigned_orders.remove(order)

        route = Route(
            depot=depot,
            orders=route_orders,
            start_time=start_time
        )

        truck.routes.append(route)
        truck.available_from = route.finish_time(shortest_paths)

    return {
        "assigned": list(set(order_list) - unassigned_orders),
        "unassigned": list(unassigned_orders)
    }


def truck_assignment(depot_list, shortest_paths):
    results = {}

    for depot in depot_list:
        results[depot] = truck_routes_for_depot(
            depot,
            depot.order_list,
            shortest_paths
        )

    for depot, result in results.items():
        print(f"\nDepot {depot.node_id}")
        print(result)

        for truck in depot.truck_list:
            print(f"Truck {truck.capacity}")

            for route in truck.routes:
                print(
                    [order.recipient_location.node_id
                     for order in route.orders]
                )
                print(
                    f"Load: {route.load()}"
                )
                print(
                    f"Distance: {route.total_distance(shortest_paths)}"
                )

    return results
