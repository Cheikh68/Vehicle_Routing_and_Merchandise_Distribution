# Vehicle Routing & Merchandise Distribution

A Python project that models a merchandise distribution system over a road network. The system assigns customer orders to depots, schedules deliveries onto trucks, and performs route optimization using graph algorithms, integer programming, and heuristic search.

The goal of the project is to explore practical approaches to solving variants of the Vehicle Routing Problem (VRP) while balancing transportation cost, truck capacity, and delivery deadlines.

---

# Features

- Model a transportation network as a weighted graph.
- Compute shortest paths between every pair of nodes using Dijkstra's algorithm.
- Assign orders to depots using Integer Linear Programming (PuLP).
- Generate truck delivery routes using a greedy heuristic.
- Support heterogeneous truck fleets with different capacities.
- Allow trucks to perform multiple routes throughout the planning horizon.
- Penalize late deliveries through a configurable cost function.
- Improve generated routes using local search (2-opt style optimization).
- Load complete scenarios from JSON files.

---

# Problem Overview

The distribution network consists of:

- Depots containing limited inventory.
- Customer nodes where orders must be delivered.
- Trucks with different carrying capacities.
- A weighted graph representing travel time between locations.
- Customer orders with:
  - destination
  - required quantity
  - delivery deadline

The objective is to deliver every order while minimizing transportation cost and lateness.

---

# Algorithm

The project is divided into three major stages.

## Part 1 — Depot Assignment (Integer Linear Programming)

Each order is assigned to exactly one depot.

The optimization minimizes total travel cost while satisfying:

- every order is assigned exactly once
- depot inventory limits are respected

This stage is solved using PuLP.

---

## Part 2 — Truck Assignment & Route Construction

For every depot:

- trucks are repeatedly dispatched until no further deliveries can be assigned
- each route is built greedily
- the next order is selected using a cost function based on:
  - travel distance
  - lateness penalty
- truck capacities are respected
- trucks may complete multiple routes during the planning period

---

## Part 3 — Route Optimization

Once the initial routes have been generated, each route is improved independently.

The optimizer performs local search by swapping delivery order within a route whenever the total route cost decreases.

The route cost combines:

- total travel distance
- total delivery lateness

---

# Technologies

- Python
- NetworkX
- PuLP
- JSON

---

# Project Structure

```text
scenario/
    scenario.json

main.py

models/
    depot.py
    truck.py
    order.py
    route.py
    node.py

algorithms/
    depot_assignment.py
    truck_assignment.py
    route_optimization.py
```

(The exact structure may differ as the project evolves.)

---

# Example Workflow

1. Load a scenario from a JSON file.
2. Construct the road network.
3. Compute all shortest paths.
4. Solve the depot assignment problem using ILP.
5. Generate delivery routes for each depot.
6. Improve routes using local optimization.
7. Display the resulting assignments and routes.

---

# Current Limitations

This project intentionally focuses on heuristic approaches rather than exact VRP optimization.

Current limitations include:

- Greedy truck assignment may not produce globally optimal routes.
- Route optimization is currently limited to intra-route improvements.
- No inter-route optimization between trucks.
- No support for split deliveries.
- No vehicle working-hour constraints.
- No pickup operations.

---

# Future Improvements

Possible future extensions include:

- Clarke-Wright Savings based initialization.
- Inter-route optimization.
- Tabu Search or Simulated Annealing.
- Genetic Algorithms.
- Time window constraints (VRPTW).
- Dynamic order arrivals.
- Multiple optimization objectives.
- Rich visualization of generated routes.

---

# License

This project was developed for educational purposes to explore optimization algorithms, graph theory, and vehicle routing heuristics.
