from typing import Generator

import simpy

from .abc import Consumer, Node, Part, Producer


class Conveyor(Node, Consumer, Producer):
    """A node that transports a part for a specified travel time before passing it on."""

    def __init__(self, env: simpy.Environment, name: str, travel_time: float = 1.0, capacity: int = 1) -> None:
        super().__init__(env, name)

        self.travel_time = travel_time
        self.resource = simpy.Resource(env, capacity=capacity)

    def set_output(self, output_target: Consumer) -> None:
        self.output_target = output_target

    def put(self, part: Part) -> None:
        """Receives a part and starts the transport process."""
        self.env.process(self.transport(part))

    def transport(self, part: Part) -> Generator:
        """The simulation process for moving a part along the conveyor."""
        with self.resource.request() as request:
            yield request
            yield self.env.timeout(self.travel_time)

        if self.output_target:
            self.output_target.put(part)
