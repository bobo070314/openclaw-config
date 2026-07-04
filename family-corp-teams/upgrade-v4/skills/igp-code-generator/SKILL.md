---
name: igp-code-generator
description: "Generates idiomatic Python code following IGP engine conventions. Includes error handling, type hints, and docstrings."
license: MIT
compatibility:
 - igp-v4
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - codes
allowed-tools:
 - read
 - write
 - exec
---

# Igp Code Generator Skill

## When to Activate
Activate this skill when the user requests Python code that must conform to IGP engine standards—e.g., implementing a new component, utility, or integration—and explicitly requires idiomatic structure, robust error handling (using `try/except` with `IGPError` where appropriate), PEP 484 type hints, and Google-style docstrings.

## Instructions
1. Parse the user’s functional specification—including inputs, outputs, side effects, and any referenced IGP interfaces or modules.
2. Generate Python code adhering to IGP v4 conventions: use `from igp import IGPError`, annotate all parameters and return types, include comprehensive docstrings with Args/Returns/Raises sections, and wrap external or unsafe operations in try-except blocks that re-raise as `IGPError` with contextual messages.
3. Ensure all functions are pure or explicitly document stateful behavior; avoid global mutable state unless required by IGP engine contract.
4. Validate generated code syntactically and semantically using `ast.parse()` and basic static checks (e.g., missing type annotations, bare `except:` clauses) before returning.
5. Output only the final `.py` code block—no explanations, no markdown wrappers—unless requested otherwise.

## Examples
```python
def fetch_sensor_data(sensor_id: str, timeout_ms: int = 5000) -> dict[str, float]:
    """Fetch real-time sensor telemetry from the IGP sensor bus.
    
    Args:
        sensor_id: Unique identifier of the sensor (e.g., 'imu_01').
        timeout_ms: Maximum wait time in milliseconds before raising timeout.
    
    Returns:
        A dictionary mapping metric names to current numeric values.
    
    Raises:
        IGPError: If sensor is unreachable, malformed response is received, or timeout occurs.
    """
    try:
        import json
        from igp import IGPError
        
        # Simulated IGP sensor bus call
        response = _call_sensor_bus(sensor_id, timeout_ms)
        if not isinstance(response, dict):
            raise IGPError(f"Invalid sensor response type for {sensor_id}: expected dict, got {type(response).__name__}")
        return response
    except TimeoutError:
        raise IGPError(f"Sensor {sensor_id} timed out after {timeout_ms}ms")
    except Exception as e:
        raise IGPError(f"Failed to fetch sensor data for {sensor_id}: {str(e)}")
```

## Notes
- This skill assumes the runtime environment has `igp` installed and accessible; it does not install dependencies.
- Never generate code that bypasses IGP security boundaries (e.g., direct filesystem writes outside `/tmp/igp/`, unvalidated `exec()` calls).
- All exceptions must be wrapped in `IGPError` (not `Exception` or built-in types) to ensure consistent error propagation across the IGP engine.