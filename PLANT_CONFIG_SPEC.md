# Plant Configuration File Specification

This document specifies the JSON format required by the `PlantBuilder` to construct a warehouse simulation environment. Adhering to this specification is crucial for the successful parsing and execution of the simulation.

## 1. Top-Level Structure

The JSON file must have a single root object with one required key: `"components"`.

```json
{
  "components": [
    // ... array of component definitions
  ]
}
```

---

## 2. Component Object

The `components` key holds an array of Component Objects. Each object defines a single node in the simulation plant and has the following structure:

| Key       | Type                          | Required? | Description                                                                                                                                 |
| :-------- | :---------------------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`    | `string`                      | **Yes**   | A unique identifier for this component instance. No two components can have the same name.                                                  |
| `type`    | `string`                      | **Yes**   | The type of the component. Must be one of the valid types listed in [Section 3](#3-component-types-and-parameters).                         |
| `params`  | `object`                      | No        | A key-value map of parameters to configure the component's behavior. Available parameters are specific to each component `type`.             |
| `outputs` | `string` or `array of strings` | No        | The `name`(s) of the downstream component(s) to which this component sends parts. A single string for one-to-one, an array for one-to-many. |

---

## 3. Component Types and Parameters

This section details the valid component `type` strings and the `params` available for each.

### `Source`
Generates parts at a regular interval.
- **`params`**:
  - `interval` (float, optional, default: `1.0`): The time (in simulation units) between part generations.
  - `limit` (integer, optional, default: `null`): The maximum number of parts to generate. If `null`, generates indefinitely.
  - `start_immediately` (boolean, optional, default: `true`): If `true`, starts generating parts at t=0.

### `Drain`
Consumes and removes parts from the simulation, recording statistics.
- **`params`**: None.

### `Conveyor`
Transports a part from one point to another, taking a specific amount of time.
- **`params`**:
  - `travel_time` (float, optional, default: `1.0`): The time it takes for a part to travel across the conveyor.
  - `capacity` (integer, optional, default: `1`): The number of parts the conveyor can transport simultaneously.

### `Station`
Represents a workstation that processes a part, taking a specific amount of time.
- **`params`**:
  - `processing_time` (float, optional, default: `1.0`): The time it takes to process one part.
  - `capacity` (integer, optional, default: `1`): The number of parts the station can process simultaneously.

### `Router`
Routes incoming parts to one of several downstream components.
- **`params`**:
  - `routing_logic` (string, optional, default: `"round_robin"`): The logic to use for routing. Valid options are `"round_robin"` and `"random"`.


---

## 4. Examples

### Valid Configuration Example

This example shows a source feeding a conveyor, which moves parts to a station. The station then sends parts to a router, which distributes them to two different drains.

```json
{
  "components": [
    {
      "name": "part_source",
      "type": "Source",
      "params": { "interval": 5.0 },
      "outputs": "entry_conveyor"
    },
    {
      "name": "entry_conveyor",
      "type": "Conveyor",
      "params": { "travel_time": 10 },
      "outputs": "processing_station"
    },
    {
      "name": "processing_station",
      "type": "Station",
      "params": { "processing_time": 8.0, "capacity": 2 },
      "outputs": "main_router"
    },
    {
      "name": "main_router",
      "type": "Router",
      "params": { "routing_logic": "round_robin" },
      "outputs": ["finished_parts_drain", "qa_inspection_drain"]
    },
    {
      "name": "finished_parts_drain",
      "type": "Drain"
    },
    {
      "name": "qa_inspection_drain",
      "type": "Drain"
    }
  ]
}
```

### Invalid Configuration Examples

**1. Duplicate Name**
```json
// INVALID: The name "main_line" is used twice.
{
  "components": [
    { "name": "main_line", "type": "Conveyor" },
    { "name": "main_line", "type": "Station" }
  ]
}
```
> **Error:** `ValueError: Duplicate component name found: main_line`

**2. Unknown Type**
```json
// INVALID: "Assembler" is not a valid component type.
{
  "components": [
    { "name": "assembly_station", "type": "Assembler" }
  ]
}
```
> **Error:** `ValueError: Unknown component type: Assembler`

**3. Unknown Output Target**
```json
// INVALID: The output "final_drain" does not exist.
{
  "components": [
    { "name": "source", "type": "Source", "outputs": "final_drain" }
  ]
}
```
> **Error:** `ValueError: Component 'source' has an unknown output target: 'final_drain'`

**4. Invalid Parameter**
```json
// INVALID: "speed" is not a valid parameter for a Conveyor.
{
  "components": [
    { 
      "name": "conveyor_1", 
      "type": "Conveyor",
      "params": { "speed": 100 }
    }
  ]
}
```
> **Error:** `TypeError: Conveyor.__init__() got an unexpected keyword argument 'speed'`
