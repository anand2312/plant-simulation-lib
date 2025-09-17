import uuid
from abc import ABC, abstractmethod
from typing import Any, TypedDict

import simpy


class Part(TypedDict):
    """Represents a part being processed in the simulation."""

    id: uuid.UUID
    creation_time: float


class Node:
    """The universal base class for any object in the simulation plant."""

    def __init__(self, env: simpy.Environment, name: str) -> None:
        self.id = uuid.uuid4()
        self.env = env
        self.name = name

        # Statistics tracking with detailed logs
        self.received_log: list[tuple[Part, float]] = []
        self.sent_log: list[tuple[Part, float]] = []

    def _record_part_received(self, part: Part) -> None:
        """Record statistics when a part is received."""
        self.received_log.append((part, self.env.now))

    def _record_part_sent(self, part: Part) -> None:
        """Record statistics when a part is sent."""
        self.sent_log.append((part, self.env.now))

    @property
    def parts_received(self) -> int:
        """Returns the total number of parts received."""
        return len(self.received_log)

    @property
    def parts_sent(self) -> int:
        """Returns the total number of parts sent."""
        return len(self.sent_log)

    def get_throughput(self) -> float:
        """Calculate throughput (parts per time unit)."""
        if self.env.now == 0:
            return 0.0
        return self.parts_received / self.env.now

    def get_average_latency(self) -> float:
        """Calculate average latency for received parts."""
        if not self.received_log:
            return 0.0

        total_latency = sum(
            arrival_time - part["creation_time"]
            for part, arrival_time in self.received_log
        )
        return total_latency / self.parts_received

    def get_max_latency(self) -> float:
        """Calculate maximum latency for received parts."""
        if not self.received_log:
            return 0.0

        return max(
            arrival_time - part["creation_time"]
            for part, arrival_time in self.received_log
        )

    def get_utilization_time(self) -> float:
        """Calculate time between first and last part received."""
        if len(self.received_log) < 2:
            return 0.0

        first_time = self.received_log[0][1]
        last_time = self.received_log[-1][1]
        return last_time - first_time


class Consumer(ABC):
    """Mixin for a Node that can receive parts."""

    @abstractmethod
    def put(self, part: Part) -> Any:
        """The method called to deliver a part to this Node."""
        pass


class Producer(ABC):
    """
    Mixin for a Node that sends parts to other Nodes.
    """

    @abstractmethod
    def set_output(self, output_target: Consumer) -> None:
        """Add a node to this producer's output set."""
        pass
