---
name: code-navigator
description: >
  Symbolic code navigation — find function definitions, class declarations,
  interface types, type aliases, enums, imports, and exports across
  TypeScript/JavaScript/Python source trees. Returns file:line references
  with snippets. Use when user asks to "find function X", "where is class Y
  defined", "show all exports of Z", "locate symbol", "navigate to definition",
  "search codebase for ..."
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Code Navigator v0.2.0

## What it does
Deep search across your source tree for symbols:
- **Functions**: `async function` / `const X = () => ...` / `function name()`
- **Classes**: `class Foo extends Bar implements Baz`
- **Interfaces**: `interface User { ... }` (TS/JS)
- **Types**: `type ID = string` (TS)
- **Enums**: `enum Status { ... }` (TS)
- **Imports**: `import X from Y` / `from X import Y` (Python)
- **Exports**: `export { ... }` / `export default ...`

Supports: `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.cjs`, `.mts`, `.cts`, `.py`

## When to use
- User says "find function ..." / "where is ... defined" / "locate symbol ..."
- "show all exports" / "navigate to class ..." / "search codebase for ..."
- "what implements interface ..." / "find all imports of ..."

## How to invoke

```bash
bash "{baseDir}/run.sh" "<project-dir>" "[symbol]" "[--type func|class|...]" "[--fuzzy]" "[--json]"
```

## Parameters
| Arg | Description |
|-----|-------------|
| `$1` | Project directory (required) |
| `$2` | Symbol name to search (optional — omit for all symbols) |
| `--type func` | Filter: func, class, interface, type, enum, import, export, all |
| `--fuzzy` | Case-insensitive substring match (regex) |
| `--json` | Output JSON instead of formatted table |

## Examples
```bash
# Find all occurrences of "createRun"
code-navigator D:/project createRun

# Find only class definitions matching "Agent"
code-navigator D:/project Agent --type class --fuzzy

# List all functions in the project
code-navigator D:/project --type func

# Export JSON for scripting
code-navigator D:/project handleSubmit --json
```

## Exit codes
- `0` = matches found and displayed
- `1` = no matches

## Context Snapshot (auto-generated)
_Scanned D:/bobo/openclaw-foreign/workspace/gh-enterprise-baseline_
### `dify\vite.config.ts`
- `defineConfig` (export)
- `import { defineConfig } from 'vite-plus'`
### `dify\api\clients\agent_backend\client.py`
- `createRun()`, `cancelRun()`, `streamEvents()` (functions)
- `AgentBackendRunClient`, `DifyAgentBackendRunClient` (classes)
### `dify\api\conftest.py`
- `pytest_addoption()`, `pytest_configure()`, `pytest_sessionstart()` (functions)
