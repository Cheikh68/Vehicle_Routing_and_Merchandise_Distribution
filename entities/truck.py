from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Truck:
    capacity: int

    current_location: "Node" = field(init=False)
    available_from: datetime = field(init=False)
    routes: list["Route"] = field(init=False)

    def __post_init__(self):
        self.available_from = datetime.min.replace(tzinfo=UTC)
        self.routes = []
