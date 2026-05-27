"""
PathSim-FMI: FMI/FMU co-simulation toolbox for PathSim

Block wrappers around the Functional Mock-up Interface (FMI 2.0 / 3.0).
The blocks load FMUs via FMPy at runtime and integrate them into a PathSim
`Simulation` either as co-simulation slaves or as model-exchange systems.
"""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

__all__ = ["__version__"]

# Block classes depend on FMPy plus the FMU's own native binary loaded via
# ctypes. Neither is available under Pyodide. FMPy itself only gets pulled
# in lazily at FMU load time, so we check for it explicitly here: when it's
# missing, the blocks aren't re-exported and introspection (e.g. PathView's
# Toolbox Manager) reports an empty toolbox instead of a class that would
# fail later at instantiation.
try:
    import fmpy  # noqa: F401  # presence check

    from .wrapper import FMUWrapper
    from .blocks import CoSimulationFMU, ModelExchangeFMU

    __all__ += ["FMUWrapper", "CoSimulationFMU", "ModelExchangeFMU"]
except ImportError:
    pass
