"""Explicit pytest plugin for the second clean Area 2 run only."""


def pytest_addoption(parser):
    parser.addoption("--area2-reverse", action="store_true", help="Reverse collected Area 2 case order")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--area2-reverse"):
        items.reverse()
