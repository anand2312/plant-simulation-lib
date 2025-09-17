import json
import logging
from pathlib import Path
from typing import Any

import simpy

from .entities.abc import Consumer, Node, Producer
from .entities.conveyor import Conveyor
from .entities.drain import Drain
from .entities.router import Router
from .entities.source import Source
from .entities.station import Station

logger = logging.getLogger(__name__)

__all__ = ["PlantBuilder"]


COMPONENT_MAP: dict[str, type[Node]] = {
    "Source": Source,
    "Drain": Drain,
    "Conveyor": Conveyor,
    "Station": Station,
    "Router": Router,
    # "Store": Store,
}


class PlantBuilder:
    """
    Builds a simulation plant from a JSON configuration file.

    This class reads a JSON file describing the components and their connections,
    instantiates the corresponding Python objects, and wires them together to create
    a runnable simulation environment.
    """

    def __init__(self, env: simpy.Environment) -> None:
        self.env = env
        self.components: dict[str, Node] = {}
        logger.debug("PlantBuilder initialized")

    def build_from_json(self, filepath: str | Path) -> dict[str, Node]:
        """
        Builds and wires a plant from a JSON config file.

        The process is done in two passes:
        1. Instantiate all component objects.
        2. Connect the outputs of producers to the inputs of consumers.
        """
        logger.info(f"Building plant from JSON config: {filepath}")
        with open(filepath, "r") as f:
            config = json.load(f)

        component_count = len(config.get("components", []))
        logger.info(f"Found {component_count} components to build")

        self._instantiate_components(config["components"])
        self._wire_components(config["components"])

        logger.info(f"Plant built successfully with {len(self.components)} components")
        return self.components

    def build_from_dict(self, obj: dict[str, Any]) -> dict[str, Node]:
        comp_count = len(obj.get("components", []))
        logger.info(f"Building plant from dict config with {comp_count} components")
        self._instantiate_components(obj["components"])
        self._wire_components(obj["components"])
        logger.info(f"Plant built successfully with {len(self.components)} components")
        return self.components

    def _instantiate_components(self, component_configs: list[dict[str, Any]]) -> None:
        logger.debug("Starting component instantiation phase")
        for config in component_configs:
            name = config["name"]
            comp_type = config["type"]
            params = config.get("params", {})

            if name in self.components:
                raise ValueError(f"Duplicate component name found: {name}")

            cls = COMPONENT_MAP[comp_type]
            component = cls(env=self.env, name=name, **params)
            self.components[name] = component

            logger.debug(f"Created {comp_type} '{name}' with params: {params}")

    def _wire_components(self, component_configs: list[dict[str, Any]]) -> None:
        logger.debug("Starting component wiring phase")
        connection_count = 0

        for config in component_configs:
            if "outputs" not in config or not config["outputs"]:
                continue

            source_name = config["name"]
            source_component = self.components[source_name]

            if not isinstance(source_component, Producer):
                raise TypeError(
                    f"Component '{source_name}' is used as an output source "
                    f"but is not a Producer."
                )

            output_names = config["outputs"]
            if isinstance(output_names, str):
                output_names = [output_names]

            for target_name in output_names:
                if target_name not in self.components:
                    raise ValueError(
                        f"Component '{source_name}' has an unknown output "
                        f"target: '{target_name}'"
                    )

                target_component = self.components[target_name]

                if not isinstance(target_component, Consumer):
                    raise TypeError(
                        f"Output target '{target_name}' is not a valid Consumer."
                    )

                source_component.set_output(target_component)
                connection_count += 1
                logger.debug(f"Connected {source_name} -> {target_name}")

        logger.info(f"Wiring completed: {connection_count} connections established")
