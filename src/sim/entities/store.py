import simpy
from simpy.resources.store import StoreGet, StorePut

from .abc import Consumer, Node, Part, Producer


class Store(Node, Consumer, Producer):
    """
    A node that acts as a buffer, holding parts until they are requested.
    It wraps a `simpy.Store`.
    """

    def __init__(
        self, env: simpy.Environment, name: str, capacity: float = float("inf")
    ) -> None:
        super().__init__(env, name)
        self.store = simpy.Store(env, capacity=capacity)

    def put(self, part: Part) -> StorePut:
        """
        Adds a part to the store. Returns a `StorePut` event that can be yielded
        to wait for the store to have available capacity.
        """
        return self.store.put(part)

    def get(self) -> StoreGet:
        """
        Creates a request to get a part from the store. Returns a `StoreGet` event
        that must be yielded by a process to wait for a part to become available.
        """
        return self.store.get()
