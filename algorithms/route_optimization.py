from entities.route import Route


def optimize_routes(shortest_paths, depot_list, ALPHA):
    print("Part 3: intra-route optimization (changing individual delivery sequences)")

    for depot in depot_list:
        print(f"Depot {depot.node_id}:")

        for truck in depot.truck_list:

            for route in truck.routes:
                if len(route.orders) < 2:
                    continue

                improved = True

                while improved:
                    improved = False

                    best_cost = route.route_cost(
                        shortest_paths,
                        ALPHA
                    )

                    for i in range(len(route.orders) - 1):
                        for j in range(i + 1, len(route.orders)):
                            candidate_orders = route.orders[:]

                            candidate_orders[i], candidate_orders[j] = (
                                candidate_orders[j],
                                candidate_orders[i]
                            )

                            candidate_route = Route(
                                depot=route.depot,
                                orders=candidate_orders,
                                start_time=route.start_time
                            )

                            candidate_cost = candidate_route.route_cost(
                                shortest_paths,
                                ALPHA
                            )

                            if candidate_cost < best_cost:
                                route.orders = candidate_orders
                                best_cost = candidate_cost
                                improved = True
                                break

                        if improved:
                            break

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
