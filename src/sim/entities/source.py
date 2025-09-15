import logging
import uuid
from typing import Generator

import simpy

from .abc import Consumer, Node, Part, Producer

logger = logging.getLogger(__name__)


class Source(Node, Producer):
    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        interval: float = 1.0,
        limit: int | None = None,
        start_immediately: bool = True,
    ) -> None:
        super().__init__(env, name)

        # Configurable parameters from the JSON file
        self.interval = interval
        self.limit = limit

        self.parts_created: int = 0

        logger.info(f"Source '{name}' initialized: interval={interval}, limit={limit}")

        if start_immediately:
            self.start()

    def set_output(self, output_target: Consumer) -> None:
        self.output_target = output_target
        target_name = getattr(output_target, "name", str(output_target))
        logger.debug(f"Source '{self.name}' output set to '{target_name}'")

    def start(self) -> None:
        """Explicitly starts the part generation process."""
        logger.info(f"Source '{self.name}' starting part generation")
        self.env.process(self.run())

    def run(self) -> Generator:
        """The main simulation process for generating parts."""
        while self.limit is None or self.parts_created < self.limit:
            # Wait for the specified interval
            yield self.env.timeout(self.interval)

            self.parts_created += 1
            part: Part = {
                "id": uuid.uuid4(),
                "creation_time": self.env.now,
            }

            if self.output_target is None:
                raise RuntimeError(f"Source '{self.name}' has no output target")

            part_id = part["id"]
            logger.debug(
                f"Source '{self.name}' created part {part_id} at T={self.env.now}"
            )
            self.output_target.put(part)

        parts_count = self.parts_created
        logger.info(f"Source '{self.name}' finished generating {parts_count} parts")
