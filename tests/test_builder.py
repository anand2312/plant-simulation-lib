from pathlib import Path

import pytest
import simpy

from sim.builder import PlantBuilder
from sim.entities.drain import Drain
from sim.entities.router import Router
from sim.entities.source import Source

TEST_DATA_DIR = Path(__file__).parent / "sample_configs"


def test_build_from_json_basic():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    components = builder.build_from_json(TEST_DATA_DIR / "basic_plant.json")

    assert "source" in components
    assert "drain" in components
    assert isinstance(components["source"], Source)
    assert isinstance(components["drain"], Drain)
    assert components["source"].output_target == components["drain"]


def test_build_from_json_full():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    components = builder.build_from_json(TEST_DATA_DIR / "full_plant.json")

    assert len(components) == 6
    assert "source" in components
    assert "conveyor" in components
    assert "station" in components
    assert "router" in components
    assert "drain1" in components
    assert "drain2" in components

    source = components["source"]
    conveyor = components["conveyor"]
    station = components["station"]
    router = components["router"]
    drain1 = components["drain1"]
    drain2 = components["drain2"]

    assert source.output_target == conveyor
    assert conveyor.output_target == station
    assert station.output_target == router
    assert isinstance(router, Router)
    assert drain1 in router.output_targets
    assert drain2 in router.output_targets


def test_build_from_dict():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    config = {
        "components": [
            {"name": "source", "type": "Source", "outputs": "drain"},
            {"name": "drain", "type": "Drain"},
        ]
    }
    components = builder.build_from_dict(config)

    assert "source" in components
    assert "drain" in components
    assert isinstance(components["source"], Source)
    assert isinstance(components["drain"], Drain)
    assert components["source"].output_target == components["drain"]


def test_build_duplicate_name_raises_error():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    with pytest.raises(ValueError, match="Duplicate component name found: source"):
        builder.build_from_json(TEST_DATA_DIR / "invalid_duplicate_name.json")


def test_build_bad_connection_raises_error():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    with pytest.raises(
        ValueError, match="has an unknown output target: 'non_existent_drain'"
    ):
        builder.build_from_json(TEST_DATA_DIR / "invalid_bad_connection.json")


def test_build_invalid_producer_raises_error():
    env = simpy.Environment()
    builder = PlantBuilder(env)
    with pytest.raises(TypeError, match="is not a Producer"):
        builder.build_from_json(TEST_DATA_DIR / "invalid_producer.json")
