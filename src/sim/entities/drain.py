import logging

import simpy

from .abc import Consumer, Node, Part

logger = logging.getLogger(__name__)


class Drain(Node, Consumer):
    def __init__(self, env: simpy.Environment, name: str) -> None:
        super().__init__(env, name)
        # Store tuples of (part, arrival_time) for statistics
        self.log: list[tuple[Part, float]] = []
        logger.info(f"Drain '{name}' initialized")

    def put(self, part: Part) -> None:
        """Receives a part and logs its arrival time."""
        self.log.append((part, self.env.now))
        part_id = part["id"]
        latency = self.env.now - part["creation_time"]
        logger.debug(
            f"Drain '{self.name}' received part {part_id} (latency={latency:.2f})"
        )

        if len(self.log) % 10 == 0:  # Log every 10 parts
            logger.info(f"Drain '{self.name}' has received {len(self.log)} parts total")

    @property
    def parts_received(self) -> int:
        """Returns the total number of parts received."""
        return len(self.log)

    def get_average_throughput(self) -> float:
        if self.env.now == 0:
            return 0.0
        return self.parts_received / self.env.now

    def get_average_latency(self) -> float:
        if not self.log:
            return 0.0

        # Latency = arrival_time - creation_time
        total_latency = sum(
            arrival_time - part["creation_time"] for part, arrival_time in self.log
        )
        return total_latency / self.parts_received
