from pathlib import Path
from typing import TypedDict

import simpy

from .builder import PlantBuilder
from .entities.abc import Node
from .entities.drain import Drain


class DrainResults(TypedDict):
    parts_received: int
    avg_throughput: float
    avg_latency: float


class Simulation:
    """
    Manages the execution of a warehouse plant simulation.
    """

    def __init__(self, env: simpy.Environment, components: dict[str, Node]) -> None:
        """
        Initializes the simulation.
        """
        self.env = env
        self.components = components

    def run(self, until: int | float) -> None:
        """
        Runs the simulation for a specified duration.
        """
        self.env.run(until=until)

    def get_results(self) -> dict[str, DrainResults]:
        """
        Collects and returns results from the simulation, primarily from Drain nodes.
        """
        results: dict[str, DrainResults] = {}
        for name, component in self.components.items():
            if isinstance(component, Drain):
                results[name] = {
                    "parts_received": component.parts_received,
                    "avg_throughput": component.get_average_throughput(),
                    "avg_latency": component.get_average_latency(),
                }
        return results

    @classmethod
    def run_from_file(
        cls, filepath: str | Path, until: int | float
    ) -> dict[str, DrainResults]:
        """
        Loads a config from a file, runs the simulation, and returns the results.
        """
        env = simpy.Environment()
        builder = PlantBuilder(env)
        components = builder.build_from_json(filepath)

        sim = cls(env, components)
        sim.run(until=until)
        return sim.get_results()
