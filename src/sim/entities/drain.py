import logging
from typing import Generator

import simpy

from .abc import Consumer, Node, Part

logger = logging.getLogger(__name__)


class Drain(Node, Consumer):
    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        capacity: int = 1,
        drain_time: float = 0.0,
    ) -> None:
        super().__init__(env, name)
        # Store tuples of (part, arrival_time) for statistics
        # self.log: list[tuple[Part, float]] = []
        self.drain_time = drain_time
        self.resource = simpy.Resource(env, capacity=capacity)
        logger.info(f"Drain '{name}' initialized")

    def put(self, part: Part) -> None:
        """Receives a part and logs its arrival time."""
        self.env.process(self.process_part_drain(part))

    def process_part_drain(self, part: Part) -> Generator:
        with self.resource.request() as request:
            part_id = part["id"]
            yield request
            self._record_part_received(part)
            yield self.env.timeout(self.drain_time)
            logger.info(
                f"Finished processing {part_id} after waiting for {self.drain_time}"
            )
            self._record_part_sent(part)
            latency = self.env.now - part["creation_time"]
            logger.debug(
                f"Drain '{self.name}' received part {part_id} (latency={latency:.2f})"
            )
