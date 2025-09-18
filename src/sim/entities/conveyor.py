import logging
from typing import Generator

import simpy

from .abc import Consumer, Node, Part, Producer, RoutingLogic

logger = logging.getLogger(__name__)


class Conveyor(Node, Consumer, Producer):
    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        travel_time: float = 1.0,
        capacity: int = 1,
        routing_strategy: RoutingLogic = "round_robin",
    ) -> None:
        super().__init__(env, name)

        self.travel_time = travel_time
        self.resource = simpy.Resource(env, capacity=capacity)
        logger.info(
            f"Conveyor '{name}' initialized: travel_time={travel_time},"
            f" capacity={capacity}"
        )

        self.routing_strategy = routing_strategy
        self.output_targets = []
        self.next_target_idx = 0

    def set_output(self, output_target: Consumer) -> None:
        self.output_targets.append(output_target)

    def put(self, part: Part) -> None:
        """Receives a part and starts the transport process."""
        self._record_part_received(part)
        part_id = part["id"]
        logger.debug(f"Conveyor '{self.name}' received part {part_id} for transport")
        self.env.process(self.transport(part))

    def transport(self, part: Part) -> Generator:
        """The simulation process for moving a part along the conveyor."""
        part_id = part["id"]

        with self.resource.request() as request:
            yield request
            logger.debug(
                f"Conveyor '{self.name}' transporting {part_id} at T={self.env.now}"
            )
            yield self.env.timeout(self.travel_time)

        logger.debug(f"Conveyor '{self.name}' completed transport of {part_id}")
        self.route_part(part)
        self._record_part_sent(part)
