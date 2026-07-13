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

---

## Example Output

```text
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                457.00000000
Enumerated nodes:               0
Total iterations:               133
Time (CPU seconds):             0.08
Time (Wallclock seconds):       0.08

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.10   (Wallclock seconds):       0.10

Part 1: Assigning orders to depots
Status: Optimal
Order 1 assigned to Depot 1
Order 2 assigned to Depot 1
Order 3 assigned to Depot 1
Order 4 assigned to Depot 1
Order 5 assigned to Depot 1
Order 6 assigned to Depot 1
Order 7 assigned to Depot 2
Order 8 assigned to Depot 2
Order 9 assigned to Depot 2
Order 10 assigned to Depot 3
Order 11 assigned to Depot 3
Order 12 assigned to Depot 2
Order 13 assigned to Depot 2
Order 14 assigned to Depot 3
Order 15 assigned to Depot 3
Order 16 assigned to Depot 3
Order 17 assigned to Depot 3
Order 18 assigned to Depot 3

Part 2: Assigning orders to trucks (for each depot)
Depot 1:
Truck 50:
[1]
Required load: 38
Distance to travel: 24
[4, 5]
Required load: 37
Distance to travel: 71
Truck 40:
[2, 3]
Required load: 40
Distance to travel: 42
Truck 30:
[6]
Required load: 28
Distance to travel: 54

Depot 2:
Truck 45:
[9, 8]
Required load: 40
Distance to travel: 39
Truck 45:
[7]
Required load: 40
Distance to travel: 30
[13]
Required load: 37
Distance to travel: 66
Truck 25:
[12]
Required load: 18
Distance to travel: 60

Depot 3:
Truck 60:
[14, 15, 17]
Required load: 60
Distance to travel: 80
Truck 35:
[16]
Required load: 19
Distance to travel: 58
[11]
Required load: 26
Distance to travel: 60
Truck 30:
[10]
Required load: 24
Distance to travel: 60
[18]
Required load: 21
Distance to travel: 90

Part 3: intra-route optimization (changing individual delivery sequences)
Depot 1:
Truck 50:
[1]
Required load: 38
Distance to travel: 24
[4, 5]
Required load: 37
Distance to travel: 71
Truck 40:
[2, 3]
Required load: 40
Distance to travel: 42
Truck 30:
[6]
Required load: 28
Distance to travel: 54

Depot 2:
Truck 45:
[9, 8]
Required load: 40
Distance to travel: 39
Truck 45:
[7]
Required load: 40
Distance to travel: 30
[13]
Required load: 37
Distance to travel: 66
Truck 25:
[12]
Required load: 18
Distance to travel: 60

Depot 3:
Truck 60:
[14, 15, 17]
Required load: 60
Distance to travel: 80
Truck 35:
[16]
Required load: 19
Distance to travel: 58
[11]
Required load: 26
Distance to travel: 60
Truck 30:
[10]
Required load: 24
Distance to travel: 60
[18]
Required load: 21
Distance to travel: 90
```

---
