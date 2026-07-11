from entities.route import Route
from entities.scenario import Scenario


def optimize_routes(scenario: Scenario):
    ALPHA = 10

    for depot in scenario.depots:
        for truck in depot.truck_list:
            for route in truck.routes:
                if len(route.orders) < 2:
                    continue

                improved = True

                while improved:
                    improved = False

                    best_cost = route.route_cost(
                        scenario.shortest_paths,
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
                                scenario.shortest_paths,
                                ALPHA
                            )

                            if candidate_cost < best_cost:
                                route.orders = candidate_orders
                                best_cost = candidate_cost
                                improved = True
                                break

                        if improved:
                            break
