import logging
from pathlib import Path
from typing import TypedDict

import simpy

from .builder import PlantBuilder
from .entities.abc import Node
from .entities.drain import Drain

logger = logging.getLogger(__name__)


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
        logger.info(
            f"Initialized simulation with {len(components)} components: "
            f"{list(components.keys())}"
        )

    def run(self, until: int | float) -> None:
        """
        Runs the simulation for a specified duration.
        """
        logger.info(f"Starting simulation run until time {until}")
        self.env.run(until=until)
        logger.info(f"Simulation completed at time {self.env.now}")

    def get_results(self) -> dict[str, DrainResults]:
        """
        Collects and returns results from the simulation, primarily from Drain nodes.
        """
        results: dict[str, DrainResults] = {}
        drain_count = 0
        for name, component in self.components.items():
            if isinstance(component, Drain):
                drain_count += 1
                parts_received = component.parts_received
                avg_throughput = component.get_average_throughput()
                avg_latency = component.get_average_latency()

                results[name] = {
                    "parts_received": parts_received,
                    "avg_throughput": avg_throughput,
                    "avg_latency": avg_latency,
                }

                logger.info(
                    f"Drain '{name}' results: {parts_received} parts, "
                    f"throughput={avg_throughput:.3f}/time, latency={avg_latency:.3f}"
                )

        logger.info(f"Collected results from {drain_count} drain components")
        return results

    @classmethod
    def run_from_file(
        cls, filepath: str | Path, until: int | float
    ) -> dict[str, DrainResults]:
        """
        Loads a config from a file, runs the simulation, and returns the results.
        """
        logger.info(f"Loading simulation from file: {filepath}")
        env = simpy.Environment()
        builder = PlantBuilder(env)
        components = builder.build_from_json(filepath)

        sim = cls(env, components)
        sim.run(until=until)
        return sim.get_results()
