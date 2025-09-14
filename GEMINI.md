# Simulation Engine (`sim/`)

This directory contains the core simulation engine for the warehouse plant, built in Python using the `simpy` library.

## Key Responsibilities

-   **Modeling**: Defines the components of the warehouse, such as workstations, conveyors, and operators, as `simpy` processes.
-   **Logic**: Implements the operational logic and workflows of the plant.
-   **State Management**: Tracks the state of the simulation and provides data to the API layer.

## Project Structure

This is a self-contained Python project managed by `uv`. It will have its own `pyproject.toml` to manage dependencies, including `simpy`.

```
sim/
├── pyproject.toml  # uv project configuration and dependencies
├── src/            # Main simulation source code
│   └── ...
└── GEMINI.md       # This file
```
