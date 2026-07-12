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

command line - C:\Users\Cheikh Saad bou Sall\PycharmProjects\Vehicle Routing & Merchandise Distribution\venv\Lib\site-packages\pulp\apis\../solverdir/cbc/win/i64/cbc.exe C:\Users\CHEIKH~1\AppData\Local\Temp\a112c594025145879591318684a4f67f-pulp.mps -timeMode elapsed -solve -printingOptions all -solution C:\Users\CHEIKH~1\AppData\Local\Temp\a112c594025145879591318684a4f67f-pulp.sol (default strategy 1)
At line 2 NAME          MODEL
At line 3 ROWS
At line 26 COLUMNS
At line 297 RHS
At line 319 BOUNDS
At line 374 ENDATA
Problem MODEL has 21 rows, 54 columns and 108 elements
Coin0008I MODEL read with 0 errors
Option for timeMode changed from cpu to elapsed
Continuous objective value is 424.667 - 0.00 seconds
Cgl0004I processed model has 21 rows, 54 columns (54 integer (54 of which binary)) and 108 elements
Cutoff increment increased from 1e-05 to 0.9999
Cbc0038I Initial state - 2 integers unsatisfied sum - 0.47619
Cbc0038I Pass   1: suminf.    0.27027 (2) obj. 425.432 iterations 2
Cbc0038I Pass   2: suminf.    0.40000 (2) obj. 455.4 iterations 4
Cbc0038I Pass   3: suminf.    0.40000 (3) obj. 456.35 iterations 4
Cbc0038I Pass   4: suminf.    0.50000 (3) obj. 455.45 iterations 4
Cbc0038I Pass   5: suminf.    1.22857 (4) obj. 520.443 iterations 11
Cbc0038I Pass   6: suminf.    0.40000 (3) obj. 514.25 iterations 3
Cbc0038I Pass   7: suminf.    0.50000 (3) obj. 513.35 iterations 5
Cbc0038I Pass   8: suminf.    0.96930 (4) obj. 539.638 iterations 13
Cbc0038I Pass   9: suminf.    0.59459 (3) obj. 541.027 iterations 5
Cbc0038I Pass  10: suminf.    0.89900 (4) obj. 594.043 iterations 5
Cbc0038I Pass  11: suminf.    0.63158 (3) obj. 598.553 iterations 4
Cbc0038I Pass  12: suminf.    1.37895 (4) obj. 598.405 iterations 5
Cbc0038I Pass  13: suminf.    0.70000 (3) obj. 612.925 iterations 6
Cbc0038I Pass  14: suminf.    0.80000 (3) obj. 612.025 iterations 4
Cbc0038I Pass  15: suminf.    0.78571 (4) obj. 580.429 iterations 13
Cbc0038I Pass  16: suminf.    0.31579 (3) obj. 577.789 iterations 6
Cbc0038I Pass  17: suminf.    0.71053 (4) obj. 541.487 iterations 6
Cbc0038I Pass  18: suminf.    0.40000 (3) obj. 535.7 iterations 6
Cbc0038I Pass  19: suminf.    0.50000 (3) obj. 536.65 iterations 6
Cbc0038I Pass  20: suminf.    1.27451 (4) obj. 551.373 iterations 14
Cbc0038I Pass  21: suminf.    0.61943 (4) obj. 562.553 iterations 4
Cbc0038I Pass  22: suminf.    1.58421 (4) obj. 581.055 iterations 10
Cbc0038I Pass  23: suminf.    0.93421 (4) obj. 597.151 iterations 1
Cbc0038I Pass  24: suminf.    1.69737 (4) obj. 574.638 iterations 7
Cbc0038I Pass  25: suminf.    1.69737 (4) obj. 574.638 iterations 0
Cbc0038I Pass  26: suminf.    1.05789 (4) obj. 554.453 iterations 10
Cbc0038I Pass  27: suminf.    0.90789 (4) obj. 554.539 iterations 2
Cbc0038I Pass  28: suminf.    0.37692 (4) obj. 680.85 iterations 17
Cbc0038I Pass  29: suminf.    0.30000 (3) obj. 680.4 iterations 2
Cbc0038I Pass  30: suminf.    0.40000 (3) obj. 679.45 iterations 7
Cbc0038I No solution found this major pass
Cbc0038I Before mini branch and bound, 10 integers at bound fixed and 0 continuous
Cbc0038I Full problem 21 rows 54 columns, reduced to 13 rows 37 columns
Cbc0038I Mini branch and bound did not improve solution (0.02 seconds)
Cbc0038I Full problem 22 rows 54 columns, reduced to 22 rows 54 columns
Cbc0038I After 0.06 seconds - Feasibility pump exiting with objective of 533 - took 0.05 seconds
Cbc0012I Integer solution of 457 found by DiveCoefficient after 133 iterations and 0 nodes (0.08 seconds)
Cbc0031I 10 added rows had average density of 26.5
Cbc0013I At root node, 10 cuts changed objective from 424.66667 to 456.99989 in 12 passes
Cbc0014I Cut generator 0 (Probing) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.001 seconds - new frequency is -100
Cbc0014I Cut generator 1 (Gomory) - 75 row cuts average 53.7 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is 1
Cbc0014I Cut generator 2 (Knapsack) - 27 row cuts average 9.9 elements, 0 column cuts (0 active)  in 0.006 seconds - new frequency is 1
Cbc0014I Cut generator 3 (Clique) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.000 seconds - new frequency is -100
Cbc0014I Cut generator 4 (MixedIntegerRounding2) - 5 row cuts average 36.0 elements, 0 column cuts (0 active)  in 0.001 seconds - new frequency is -100
Cbc0014I Cut generator 5 (FlowCover) - 0 row cuts average 0.0 elements, 0 column cuts (0 active)  in 0.001 seconds - new frequency is -100
Cbc0014I Cut generator 6 (TwoMirCuts) - 61 row cuts average 31.7 elements, 0 column cuts (0 active)  in 0.003 seconds - new frequency is 1
Cbc0014I Cut generator 7 (ZeroHalf) - 5 row cuts average 18.2 elements, 0 column cuts (0 active)  in 0.001 seconds - new frequency is -100
Cbc0001I Search completed - best objective 457, took 133 iterations and 0 nodes (0.08 seconds)
Cbc0035I Maximum depth 0, 0 variables fixed on reduced cost
Cuts at root node changed objective from 424.667 to 457
Probing was tried 12 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.001 seconds)
Gomory was tried 12 times and created 75 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
Knapsack was tried 12 times and created 27 cuts of which 0 were active after adding rounds of cuts (0.006 seconds)
Clique was tried 12 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.000 seconds)
MixedIntegerRounding2 was tried 12 times and created 5 cuts of which 0 were active after adding rounds of cuts (0.001 seconds)
FlowCover was tried 12 times and created 0 cuts of which 0 were active after adding rounds of cuts (0.001 seconds)
TwoMirCuts was tried 12 times and created 61 cuts of which 0 were active after adding rounds of cuts (0.003 seconds)
ZeroHalf was tried 12 times and created 5 cuts of which 0 were active after adding rounds of cuts (0.001 seconds)

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
