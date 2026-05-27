"""Skip helpers for FMU integration tests.

PathSim's pre-3.0 reference FMUs ship `darwin64` binaries that are x86_64
only. An arm64 Python (Apple Silicon) can't load them via ctypes, so the
affected tests are skipped on that platform. Linux and Windows CI runs
the full suite. Tests that only exercise pure-Python code paths (import
error checks, dataclass tests) keep running everywhere.
"""

import platform
import pytest

_DARWIN_ARM = platform.system() == "Darwin" and platform.machine() == "arm64"

# Test classes that load a pathsim-core legacy FMU (darwin64-only) at setUp.
# Tests inside these classes can't run on Apple Silicon without Rosetta.
_DARWIN_INCOMPATIBLE_CLASSES = {
    "TestFMUWrapperCoSimulation",
    "TestFMUWrapperModelExchange",
    "TestCoSimFMUSystem",
    "TestModelExchangeFMUBouncingBall",
    "TestModelExchangeFMUVanDerPol",
    "TestModelExchangeFMUBlockAPI",
}


def pytest_collection_modifyitems(config, items):
    if not _DARWIN_ARM:
        return
    skip_marker = pytest.mark.skip(
        reason="legacy FMU binary is x86_64-darwin only; can't load on Apple Silicon"
    )
    for item in items:
        cls = getattr(item, "cls", None)
        if cls is not None and cls.__name__ in _DARWIN_INCOMPATIBLE_CLASSES:
            item.add_marker(skip_marker)
