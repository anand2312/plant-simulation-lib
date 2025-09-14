import simpy

from .abc import Consumer, Node, Part


class Drain(Node, Consumer):
    """A node that consumes parts, storing them and recording statistics for later retrieval."""

    def __init__(self, env: simpy.Environment, name: str) -> None:
        super().__init__(env, name)
        # Store tuples of (part, arrival_time) for statistics
        self.log: list[tuple[Part, float]] = []

    def put(self, part: Part) -> None:
        """Receives a part and logs its arrival time."""
        self.log.append((part, self.env.now))

    @property
    def parts_received(self) -> int:
        """Returns the total number of parts received."""
        return len(self.log)

    def get_average_throughput(self) -> float:
        """Calculates the average throughput of parts arriving at the drain since t=0."""
        if self.env.now == 0:
            return 0.0
        return self.parts_received / self.env.now

    def get_average_latency(self) -> float:
        """Calculates the average time parts spent in the system before arriving here."""
        if not self.log:
            return 0.0
        
        # Latency = arrival_time - creation_time
        total_latency = sum(arrival_time - part['creation_time'] for part, arrival_time in self.log)
        return total_latency / self.parts_received
