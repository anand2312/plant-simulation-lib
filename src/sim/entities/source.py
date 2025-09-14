from typing import Generator
import uuid

import simpy

from .abc import Consumer, Node, Part, Producer


class Source(Node, Producer):
    """A node that generates parts at a specified interval and sends them to an output."""

    def __init__(self, env: simpy.Environment, name: str, interval: float = 1.0, limit: int | None = None, start_immedietely: bool = True) -> None:
        super().__init__(env, name)

        # Configurable parameters from the JSON file
        self.interval = interval
        self.limit = limit

        self.parts_created: int = 0
    
        if start_immedietely:
            self.start()
    
    def set_output(self, output_target: Consumer) -> None:
        self.output_target = output_target

    def start(self) -> None:
        """Explicitly starts the part generation process."""
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

            if self.output_target:
                self.output_target.put(part)
