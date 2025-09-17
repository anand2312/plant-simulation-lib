import logging
from pathlib import Path
from typing import TypedDict

import simpy

from .builder import PlantBuilder
from .entities.abc import Node

logger = logging.getLogger(__name__)


class ComponentStats(TypedDict):
    parts_received: int
    parts_sent: int
    throughput: float
    avg_latency: float
    max_latency: float
    utilization_time: float


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

    def get_results(self) -> dict[str, ComponentStats]:
        """
        Collects and returns statistics from all simulation components.
        """
        results: dict[str, ComponentStats] = {}

        for name, component in self.components.items():
            parts_received = component.parts_received
            parts_sent = component.parts_sent
            throughput = component.get_throughput()
            avg_latency = component.get_average_latency()
            max_latency = component.get_max_latency()
            utilization_time = component.get_utilization_time()

            results[name] = {
                "parts_received": parts_received,
                "parts_sent": parts_sent,
                "throughput": throughput,
                "avg_latency": avg_latency,
                "max_latency": max_latency,
                "utilization_time": utilization_time,
            }

            logger.info(
                f"Component '{name}' stats: received={parts_received}, "
                f"sent={parts_sent}, throughput={throughput:.3f}/time, "
                f"avg_latency={avg_latency:.3f}, max_latency={max_latency:.3f}, "
                f"utilization={utilization_time:.3f}"
            )

        logger.info(f"Collected statistics from {len(results)} components")
        return results

    @classmethod
    def run_from_file(
        cls, filepath: str | Path, until: int | float
    ) -> dict[str, ComponentStats]:
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
