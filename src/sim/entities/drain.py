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
        self._record_part_received(part)
        self.log.append((part, self.env.now))
        part_id = part["id"]
        latency = self.env.now - part["creation_time"]
        logger.debug(
            f"Drain '{self.name}' received part {part_id} (latency={latency:.2f})"
        )
