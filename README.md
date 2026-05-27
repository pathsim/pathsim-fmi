<p align="center">
  <img src="https://raw.githubusercontent.com/pathsim/pathsim-fmi/master/docs/source/logos/fmi_logo.png" width="300" alt="PathSim-FMI Logo" />
</p>

<p align="center">
  <strong>FMI/FMU co-simulation toolbox for PathSim</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/pathsim-fmi/"><img src="https://img.shields.io/pypi/v/pathsim-fmi" alt="PyPI"></a>
  <img src="https://img.shields.io/github/license/pathsim/pathsim-fmi" alt="License">
</p>

<p align="center">
  <a href="https://pathsim.org">Homepage</a> &bull;
  <a href="https://docs.pathsim.org/fmi">Documentation</a> &bull;
  <a href="https://github.com/pathsim/pathsim-fmi">GitHub</a>
</p>

---

PathSim-FMI extends the [PathSim](https://github.com/pathsim/pathsim)
simulation framework with block wrappers around the
[Functional Mock-up Interface](https://fmi-standard.org/) (FMI 2.0 / 3.0).
Drop an `.fmu` file into a PathSim simulation as either a co-simulation slave
or as a model-exchange system driven by PathSim's own integrators. Built on
top of [FMPy](https://github.com/CATIA-Systems/FMPy).

## Blocks

| Block | Description | Key Parameters |
|-------|-------------|----------------|
| `CoSimulationFMU` | Wrap a Co-Simulation FMU, advanced on a fixed grid `dt` via `fmi*DoStep` | `fmu_path`, `dt`, `start_values` |
| `ModelExchangeFMU` | Wrap a Model-Exchange FMU, integrated by PathSim's solver of choice | `fmu_path`, `start_values` |

Both blocks build on `FMUWrapper`, a lower-level version-agnostic wrapper
around FMPy (FMI 2.0 / 3.0) that you can use directly if you need finer
control than the block API offers.

## Install

```bash
pip install pathsim-fmi
```

In the PathView web app: install fails on purpose (the FMU runtime needs to
load a native binary via `ctypes`, which Pyodide can't provide). Use the
standalone PathView desktop app or any local Python environment.

## Quick Example

```python
from pathsim import Simulation, Connection
from pathsim.blocks import Scope
from pathsim_fmi import ModelExchangeFMU

fmu = ModelExchangeFMU("VanDerPol.fmu")
sco = Scope(labels=["x0", "x1"], sampling_period=0.02)

sim = Simulation(
    blocks=[fmu, sco],
    connections=[
        Connection(fmu[0], sco[0]),
        Connection(fmu[1], sco[1]),
    ],
    dt=0.01,
)
sim.run(5.0)
sco.plot()
```

## Development

```bash
pip install -e ".[test]" fmpy ruff mypy
ruff check src/ tests/      # lint
ruff format src/ tests/     # format
mypy src/pathsim_fmi        # type check
pytest tests/ -v            # run tests
```

The test suite uses the official [Modelica Reference-FMUs](https://github.com/modelica/Reference-FMUs)
under `tests/data/reference/` for portable smoke tests, plus a handful of
legacy FMUs (under `tests/data/`) carried over from pathsim-core. The legacy
FMUs ship `darwin64` binaries that are x86_64 only, so the corresponding
tests are auto-skipped on Apple Silicon; CI on Linux runs the full suite.

## License

MIT
