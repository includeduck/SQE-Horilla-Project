"""Deterministic distributed collection and independent reversed execution."""
import hashlib


def pytest_addoption(parser):
    parser.addoption("--area2-reverse", action="store_true", default=False)
    parser.addoption("--area2-shards", type=int, default=1)
    parser.addoption("--area2-shard", type=int, default=0)


def pytest_collection_modifyitems(config, items):
    total, index = config.getoption("--area2-shards"), config.getoption("--area2-shard")
    if total < 1 or not 0 <= index < total:
        raise ValueError("Invalid shard index/count")
    if total > 1:
        selected, other = [], []
        for item in items:
            bucket = int(hashlib.sha256(item.nodeid.encode()).hexdigest(), 16) % total
            (selected if bucket == index else other).append(item)
        config.hook.pytest_deselected(items=other)
        items[:] = selected
    if config.getoption("--area2-reverse"):
        items.reverse()
