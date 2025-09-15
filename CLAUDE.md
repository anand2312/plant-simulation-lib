# Simulation Engine

Python-based warehouse plant simulation using simpy and uv.

## Key Components
- **Modeling**: Workstations, conveyors, operators as simpy processes
- **Logic**: Plant operational workflows
- **State Management**: Simulation state tracking for API layer

## Development Commands
- `uv run python -m src.main` - Run simulation
- `uv run pytest` - Run tests
- `uv run ruff check` - Lint code
- `uv run ruff format` - Format code
- `uv sync` - Sync dependencies

## Project Structure
- `src/` - Main simulation source code
- `tests/` - Test files
- `pyproject.toml` - uv project config

## Dependencies
Managed by uv in pyproject.toml. Key dependencies:
- simpy - Discrete event simulation
- Additional packages as needed for modeling