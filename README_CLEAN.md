# Qupac (Quantum Python Abstraction Compiler)

A lightweight language to design quantum circuits and transpile them to Python code using Qiskit 2.x. Write simple gate instructions; Qupac parses, transpiles, and can run the generated Python for simulation.

## Highlights
- Minimal syntax for qubit/classical declarations, gate application, measurement, and simulate.
- CLI runs generated Python in the background by default on Windows.
- Optionally emit the generated Python without running it.

## Project layout
- `qupac/grammar.lark` — Lark grammar for the language
- `qupac/parser.py` — Parser and transformer to an IR
- `qupac/transpiler.py` — IR -> Python (Qiskit 2.x) code generator
- `qupac/executor.py` — Runs generated Python (bg/fg)
- `qupac/cli.py` — CLI entrypoint (background by default)

## Language quick reference
- Use statement: `use qiskit`
- Qubits: `qubits: <int>`
- Classical bits (optional): `classical: <int>`
- Apply gate: `apply H to 0` or `apply CX from 0 to 1`
  - Entangle two qubits: `entangle 0,1` (shorthand for `apply CX from 0 to 1`)
  - Put a qubit in superposition: `superpose 0` (shorthand for `apply H to 0`)
  - Gate modifiers: `apply H inv to 0` (inverse) or `apply X power(2) to 0` (power)
- Parameterized gates: `apply RX(pi/2) to 0` or `apply U(theta, phi, lambda) to 0`
  - Rotation gates: `RX`, `RY`, `RZ`, `P` (phase)
  - Universal gate: `U(theta, phi, lambda)`
  - Controlled phase: `apply CP(pi/4) from 0 to 1`
- Additional single-qubit gates: `I` (identity), `Sdg` (S-dagger), `Tdg` (T-dagger), `SX` (sqrt-X), `SXdg` (sqrt-X-dagger)
- Barrier: `barrier` (full circuit) or `barrier 0,2` (specific qubits)
- Global phase: `phase: pi/4`
- Measure all: `measure all`
- Measure one: `measure 0 -> 0`
- Execute: `simulate`
  - Shots (number of measurement samples): `shots: 1024` (default 1024 if not provided)
  - Optimization level for transpile: `optimize: 0|1|2|3` (maps to Qiskit's optimization_level)
  - Draw the generated circuit: `draw` or `draw mpl` (text drawing is default; `mpl` attempts a matplotlib rendering)
- Simulator backend method: `simulator: default|statevector|unitary`
- Simple noise model (depolarizing): `noise depol p=0.01` (requires qiskit-aer noise modules)
- Comments: lines starting with `#` or `//`

## Examples

Basic Bell state:
```
use qiskit
qubits: 2
entangle 0,1
measure all
simulate
```

Superposition:
```
use qiskit
qubits: 1
superpose 0
measure all
simulate
```

Universal gate (U gate with 3 parameters):
```
use qiskit
qubits: 1
# U(theta, phi, lambda) - general single-qubit unitary
apply U(pi/2, 0, pi) to 0
measure all
simulate
```

Phase gate and controlled-phase:
```
use qiskit
qubits: 2
# Apply phase rotation
apply P(pi/4) to 0
# Controlled-phase gate
apply CP(pi/2) from 0 to 1
measure all
simulate
```

Gate modifiers (inverse and power):
```
use qiskit
qubits: 2
apply H to 0
apply H inv to 0  # H^-1 (inverse)
apply X power(2) to 1  # X^2
measure all
simulate
```

Additional single-qubit gates:
```
use qiskit
qubits: 1
apply Sdg to 0  # S-dagger (S^-1)
apply Tdg to 0  # T-dagger (T^-1)
apply SX to 0   # sqrt(X)
apply SXdg to 0 # sqrt(X)-dagger
measure all
simulate
```

Barriers and global phase:
```
use qiskit
qubits: 3
phase: pi/8
superpose 0
barrier  # barrier on all qubits
entangle 0,1
barrier 0,1  # barrier on specific qubits
apply H to 2
measure all
simulate
```

Draw and simulation options:
```
use qiskit
qubits: 2
entangle 0,1
draw
shots: 2048
optimize: 1
simulate
```

Parameterized rotation gates:
```
use qiskit
qubits: 1
apply RX(pi/2) to 0
apply RY(pi/3) to 0
apply RZ(pi/4) to 0
draw
simulator: statevector
shots: 1
simulate
```

Noise (depolarizing):
```
use qiskit
qubits: 2
entangle 0,1
noise depol p=0.02
shots: 2048
simulate
```

## Setup
1) Create and activate a Python 3.9+ environment.
2) Install dependencies (Qiskit is large; installing only Lark lets you test parsing/transpiling):
   - Minimal (parser/transpiler only):
     pip install lark
   - Full (to actually run/simulate):
     pip install -r requirements.txt

## Developer setup (lint, type-check, tests)
- Using pip extras:
  pip install -e .[dev]
- Or individually:
  pip install ruff mypy pytest

- Lint (Ruff):
  ruff check .
- Type check (mypy):
  mypy qupac
- Run tests (pytest):
  pytest -q

## How to run
- Emit generated Python (no Qiskit needed):
  python -m qupac.cli --emit examples/main.qu
- Run generated Python in the background (requires Qiskit installed):
  python -m qupac.cli examples/main.qu
- Run in foreground/blocking (requires Qiskit installed):
  python -m qupac.cli --fg examples/main.qu

## License
MIT
