import logging
from typing import Generator

import simpy

from .abc import Consumer, Node, Part, Producer

logger = logging.getLogger(__name__)


class Station(Node, Consumer, Producer):
    """A node that processes a part, requiring a resource and taking time."""

    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        processing_time: float = 1.0,
        capacity: int = 1,
    ) -> None:
        super().__init__(env, name)

        self.output_target: Consumer | None = None
        self.processing_time = processing_time
        self.resource = simpy.Resource(env, capacity=capacity)

        logger.info(
            f"Station '{name}' initialized: processing_time={processing_time}"
            f", capacity={capacity}"
        )

    def set_output(self, output_target: Consumer) -> None:
        self.output_target = output_target

    def put(self, part: Part) -> None:
        """Receives a part and starts the processing workflow."""
        self._record_part_received(part)
        part_id = part["id"]
        logger.debug(f"Station '{self.name}' received part {part_id} for processing")
        self.env.process(self.process_part(part))

    def process_part(self, part: Part) -> Generator:
        """The simulation process for processing a single part."""
        part_id = part["id"]

        with self.resource.request() as request:
            logger.debug(f"Station '{self.name}' waiting for resource for {part_id}")
            yield request

            logger.debug(
                f"Station '{self.name}' processing {part_id} at T={self.env.now}"
            )
            yield self.env.timeout(self.processing_time)

            logger.debug(
                f"Station '{self.name}' completed {part_id} at T={self.env.now}"
            )

        if self.output_target:
            self._record_part_sent(part)
            self.output_target.put(part)
