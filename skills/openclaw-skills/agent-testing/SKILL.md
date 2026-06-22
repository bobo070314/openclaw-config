---
name: agent-testing
description: "End-to-end test runner — auto-detects pytest/vitest/jest/cargo/go, runs tests and reports pass/fail/skip counts with timing. Use when user says 'run tests', 'test the project', 'execute test suite', 'verify tests pass'."
metadata:
  openclaw:
    requires:
      bins: ["python"]
---

# Agent Testing Suite v0.2.0

## What's new in v0.2.0
- **Multi-framework**: auto-detects pytest, vitest, jest, cargo test, go test
- **Structured output**: pass/fail/skip counts with timing
- **Pattern filtering**: `--framework` override and test name pattern support
- **Cross-platform**: Python-based runner with bash/bat wrappers

## When to use
- User says "run the tests" / "execute test suite" / "test this project"
- Need to verify test pass rate before PR
- Want to run a specific test pattern (`test_auth`, `login flow`)

## How to invoke

```bash
bash "{baseDir}/run.sh" "<project-dir>" "[test-pattern]" "[--framework pytest]"
```

## Parameters
- `$1` = project directory path (required)
- `$2` = test name pattern (optional, e.g. `test_login`)
- `--framework <name>` = override auto-detection (optional)

## Supported frameworks
| Framework | Detected by |
|-----------|-------------|
| pytest | pytest.ini, pyproject.toml, setup.cfg, tests/ dir |
| vitest | vitest.config.ts/js, package.json |
| jest | jest.config.ts/js/json, package.json |
| cargo test | Cargo.toml |
| go test | go.mod |

## Exit codes
- `0` = all tests passed
- `1` = tests failed or framework not found
