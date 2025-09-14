from abc import ABC, abstractmethod
from typing import TypedDict, Any
import uuid

import simpy


class Part(TypedDict):
    """Represents a part being processed in the simulation."""
    id: uuid.UUID
    creation_time: float


class Node:
    """The universal base class for any object in the simulation plant."""

    def __init__(self, env: simpy.Environment, name: str) -> None:
        self.id = uuid.uuid4()
        self.env = env
        self.name = name



class Consumer(ABC):
    """Mixin for a Node that can receive parts."""

    @abstractmethod
    def put(self, part: Part) -> Any:
        """The method called to deliver a part to this Node."""
        pass


class Producer(ABC):
    """
    Mixin for a Node that sends parts to other Nodes.
    """
    @abstractmethod
    def set_output(self, output_target: Consumer) -> None:
        """Add a node to this producer's output set."""
        pass