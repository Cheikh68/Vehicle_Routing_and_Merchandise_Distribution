from datetime import timedelta
from entities.route import Route


def truck_routes_for_depot(depot, order_list, shortest_paths, ALPHA, BETA, GAMMA):
    unassigned_orders = set(order_list)

    def get_best_order(current_node, current_time, remaining_truck_capacity, truck_capacity):
        best_order = None
        best_cost = float("inf")

        for order in unassigned_orders:

            # Does order fit to begin with
            if order.required_amount > remaining_truck_capacity:
                continue

            # Penalty for longer distances
            travel = shortest_paths[current_node][order.recipient_location]["length"]

            # Penalty for lateness
            arrival = current_time + timedelta(minutes=travel)
            lateness = max(0, (arrival - order.deadline).total_seconds() / 60)

            # Reward closer to full capacity
            route_progress = 1 - remaining_truck_capacity / truck_capacity
            fill_ratio = (truck_capacity - remaining_truck_capacity + order.required_amount) / truck_capacity
            fill_reward = route_progress * fill_ratio

            # Reward orders with most nearby unassigned orders
            cluster_score = sum(
                1
                for o in unassigned_orders
                if o is not order
                and shortest_paths[order.recipient_location][o.recipient_location]["length"] <= 15
            )

            # Final cost calculation
            cost = travel + (ALPHA * lateness) - (BETA * fill_reward) - (GAMMA * cluster_score)
            if cost < best_cost:
                best_cost = cost
                best_order = order

        return best_order

    # Continue until every order has been assigned
    while unassigned_orders:

        # Truck that becomes available the earliest
        truck = min(
            depot.truck_list,
            key=lambda t: (t.available_from, -t.capacity)
        )

        start_time = truck.available_from
        current_node = depot
        current_time = start_time
        remaining_capacity = truck.capacity

        route_orders = []

        while True:

            order = get_best_order(
                current_node,
                current_time,
                remaining_capacity,
                truck.capacity
            )

            if order is None:
                break

            travel = shortest_paths[current_node][order.recipient_location]["length"]

            current_time += timedelta(minutes=travel)

            remaining_capacity -= order.required_amount

            current_node = order.recipient_location

            route_orders.append(order)

            unassigned_orders.remove(order)

        # This truck cannot take any remaining order
        if not route_orders:
            break

        route = Route(
            depot=depot,
            orders=route_orders,
            start_time=start_time
        )

        truck.routes.append(route)

        truck.available_from = route.finish_time(shortest_paths)


def truck_assignment(depot_list, shortest_paths, ALPHA, BETA, GAMMA):
    for depot in depot_list:
        truck_routes_for_depot(
            depot,
            depot.order_list,
            shortest_paths,
            ALPHA,
            BETA,
            GAMMA
        )

    print("\nPart 2: Assigning orders to trucks (for each depot)")
    for depot in depot_list:
        print(f"Depot {depot.node_id}:")

        for truck in depot.truck_list:
            print(f"Truck {truck.capacity}:")

            for route in truck.routes:
                print(
                    [order.order_id
                     for order in route.orders]
                )
                print(
                    f"Required load: {route.load()}"
                )
                print(
                    f"Distance to travel: {route.total_distance(shortest_paths)}"
                )

        print()
