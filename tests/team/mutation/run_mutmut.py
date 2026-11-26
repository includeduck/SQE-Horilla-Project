"""Run mutmut with the team's custom business-rule operators, scoped to the
15 business-logic functions of the two workflows.

Usage (WSL / Linux, from the repo root, with the project venv):
    python tests/team/mutation/run_mutmut.py run          # scoped run
    python tests/team/mutation/run_mutmut.py results      # any mutmut subcommand
    python tests/team/mutation/run_mutmut.py show NAME

`run` without mutant names is restricted to the functions in
tests/team/unit/coverage_scope.py (SCOPE); pass explicit names to override.
"""

import importlib.util
import sys
from pathlib import Path

from mutmut.mutation import mutators

TEAM = Path(__file__).resolve().parents[1]


def _load(name, path):
    # Load by file path under a private name: mutmut runs pytest in this same
    # process inside mutants/, and a pre-imported `unit`/`mutation` package from
    # the original tree would clash with the copies pytest imports there.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CUSTOM_OPERATORS = _load("_sqe_custom_operators", TEAM / "mutation" / "custom_operators.py").CUSTOM_OPERATORS
SCOPE = _load("_sqe_coverage_scope", TEAM / "unit" / "coverage_scope.py").SCOPE

# Register the business-rule operators inside mutmut itself (same list object
# that mutmut's file_mutation module iterates over).
mutators.mutation_operators.extend(CUSTOM_OPERATORS)


def mutmut_name_glob(file, qualname):
    """mutmut 3 names: module.x_func__mutmut_N or module.xǁClassǁmethod__mutmut_N."""
    module = file[:-3].replace("/", ".")
    if "." in qualname:
        cls, meth = qualname.split(".")
        return f"{module}.xǁ{cls}ǁ{meth}__mutmut_*"
    return f"{module}.x_{qualname}__mutmut_*"


SCOPED_GLOBS = [mutmut_name_glob(f, q) for f, q, _ in SCOPE]

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["run"] and len(args) == 1:
        args += SCOPED_GLOBS
    if args[:1] == ["globs"]:
        print("\n".join(SCOPED_GLOBS))
        sys.exit(0)
    from mutmut.__main__ import cli

    sys.exit(cli(args))
