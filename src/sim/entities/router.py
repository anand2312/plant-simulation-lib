import logging
import random
from typing import Literal

import simpy

from .abc import Consumer, Node, Part, Producer

logger = logging.getLogger(__name__)

RoutingLogic = Literal["round_robin", "random"]


class Router(Node, Consumer, Producer):
    """A node that routes a part to one of several outputs based on a defined logic."""

    def __init__(
        self,
        env: simpy.Environment,
        name: str,
        routing_logic: RoutingLogic = "round_robin",
    ) -> None:
        super().__init__(env, name)

        self.output_targets: list[Consumer] = []
        self.logic = routing_logic
        self.next_target_idx = 0

        logger.info(f"Router '{name}' initialized with {routing_logic} logic")

    def set_output(self, output_target: Consumer) -> None:
        self.output_targets.append(output_target)

    def put(self, part: Part) -> None:
        """Receives a part and routes it to a downstream component."""
        part_id = part["id"]

        if not self.output_targets:
            logger.warning(
                f"Router '{self.name}' discarding part {part_id} - no outputs"
            )
            return

        if self.logic == "round_robin":
            target = self.output_targets[self.next_target_idx]
            target_name = getattr(target, "name", str(target))
            logger.debug(
                f"Router '{self.name}' routing {part_id} to {target_name} (round_robin)"
            )
            target.put(part)
            self.next_target_idx = (self.next_target_idx + 1) % len(self.output_targets)

        elif self.logic == "random":
            target = random.choice(self.output_targets)
            target_name = getattr(target, "name", str(target))
            logger.debug(
                f"Router '{self.name}' routing {part_id} to {target_name} (random)"
            )
            target.put(part)

        else:
            target = self.output_targets[0]
            target_name = getattr(target, "name", str(target))
            logger.debug(
                f"Router '{self.name}' routing {part_id} to {target_name} (default)"
            )
            target.put(part)
