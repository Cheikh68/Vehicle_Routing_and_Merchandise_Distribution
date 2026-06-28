from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Order:
    order_id: int
    required_amount: int
    recipient_location: "Node"

    deadline: datetime = field(init=False, default=datetime(2026, 6, 1, 11, 0, tzinfo=UTC))

    def __hash__(self):
        return hash(self.order_id)

    def __eq__(self, other):
        return isinstance(other, Order) and self.order_id == other.order_id
