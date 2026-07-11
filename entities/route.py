from dataclasses import dataclass
from datetime import timedelta, datetime


@dataclass
class Route:
    depot: "Depot"
    orders: list["Order"]
    start_time: datetime

    def load(self):
        return sum(order.required_amount for order in self.orders)

    def total_distance(self, shortest_paths):
        if not self.orders:
            return 0

        distance = 0

        # depot -> first order
        distance += shortest_paths[
            self.depot
        ][
            self.orders[0].recipient_location
        ]["length"]

        # between orders
        for i in range(len(self.orders) - 1):
            distance += shortest_paths[
                self.orders[i].recipient_location
            ][
                self.orders[i + 1].recipient_location
            ]["length"]

        # last order -> depot
        distance += shortest_paths[
            self.orders[-1].recipient_location
        ][
            self.depot
        ]["length"]

        return distance

    def finish_time(self, shortest_paths):
        current = self.depot
        current_time = self.start_time

        for order in self.orders:
            travel = shortest_paths[
                current
            ][
                order.recipient_location
            ]["length"]

            current_time += timedelta(minutes=travel)
            current = order.recipient_location

        # return to depot
        current_time += timedelta(
            minutes=shortest_paths[current][self.depot]["length"]
        )

        return current_time

    def total_lateness(self, shortest_paths):
        current = self.depot
        current_time = self.start_time

        lateness = 0

        for order in self.orders:
            travel = shortest_paths[current][order.recipient_location]["length"]
            current_time += timedelta(minutes=travel)

            lateness += max(
                0,
                (current_time - order.deadline).total_seconds() / 60
            )

            current = order.recipient_location

        return lateness

    def route_cost(self, shortest_paths, alpha):
        return (
            self.total_distance(shortest_paths)
            + alpha * self.total_lateness(shortest_paths)
        )

    def copy(self):
        return Route(
            depot=self.depot,
            orders=self.orders.copy(),
            start_time=self.start_time
        )
