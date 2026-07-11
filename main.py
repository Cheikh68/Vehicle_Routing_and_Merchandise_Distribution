from algorithms.depot_assignment_ILP import assign_order_to_depot
from algorithms.truck_assignment import truck_assignment
from algorithms.route_optimization import optimize_routes
from entities.scenario import Scenario

if __name__ == '__main__':
    scenario = Scenario("data/scenario1.json")
    depot_assignment = assign_order_to_depot(scenario.depots, scenario.shortest_paths, scenario.orders)
    truck_assignment = truck_assignment(scenario.depots, scenario.shortest_paths)
    optimize_routes(scenario)
