from typing import Literal
import random

import simpy

from .abc import Consumer, Node, Part, Producer

RoutingLogic = Literal["round_robin", "random"]


class Router(Node, Consumer, Producer):
    """A node that routes a part to one of several outputs based on a defined logic."""

    def __init__(self, env: simpy.Environment, name: str, routing_logic: RoutingLogic = "round_robin") -> None:
        super().__init__(env, name)

        self.output_targets: list[Consumer] = []

        self.logic = routing_logic
        self.next_target_idx = 0

    def set_output(self, output_target: Consumer) -> None:
        self.output_targets.append(output_target)
    
    def put(self, part: Part) -> None:
        """Receives a part and routes it to a downstream component."""
        if not self.output_targets:
            # No outputs configured, so the part is discarded.
            return

        if self.logic == "round_robin":
            target = self.output_targets[self.next_target_idx]
            target.put(part)
            self.next_target_idx = (self.next_target_idx + 1) % len(self.output_targets)

        elif self.logic == "random":
            target = random.choice(self.output_targets)
            target.put(part)

        else:
            # If logic is unknown or unsupported, default to the first output
            self.output_targets[0].put(part)
