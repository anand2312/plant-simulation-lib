from typing import Generator

import simpy

from .abc import Consumer, Node, Part, Producer


class Station(Node, Consumer, Producer):
    """A node that processes a part, requiring a resource and taking time."""

    def __init__(self, env: simpy.Environment, name: str, processing_time: float = 1.0, capacity: int = 1) -> None:
        super().__init__(env, name)

        self.output_target: Consumer | None = None
        self.processing_time = processing_time
        self.resource = simpy.Resource(env, capacity=capacity)
    
    def set_output(self, output_target: Consumer) -> None:
        self.output_target = output_target

    def put(self, part: Part) -> None:
        """Receives a part and starts the processing workflow."""
        self.env.process(self.process_part(part))

    def process_part(self, part: Part) -> Generator:
        """The simulation process for processing a single part."""
        with self.resource.request() as request:
            yield request
            yield self.env.timeout(self.processing_time)

        if self.output_target:
            self.output_target.put(part)
