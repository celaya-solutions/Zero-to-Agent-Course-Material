"""One package, four rooms: every room resolves the clone the same way."""
import importlib.util
import re
import subprocess
import sys

import pytest

import zta
from zta.storage import root

ROOMS = {
    "watchman": "projects/watchman/watch.py",
    "watchman_manage": "projects/watchman/manage.py",
    "local_models": "projects/local-models/lab.py",
    "front_desk": "projects/front-desk/desk.py",
}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, root()/relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_package_is_not_nested_inside_a_room():
    """A pull leaves ignored caches behind under the old home; only source matters."""
    assert (root()/"projects/zta/src/zta").is_dir()
    assert [p.name for p in (root()/"projects/documents").rglob("*.py")] == []
    assert zta.__file__.startswith(str(root()/"projects/zta/src/zta"))


@pytest.mark.parametrize("name,relative", sorted(ROOMS.items()))
def test_room_resolves_the_same_repository_root(name, relative):
    assert load(name, relative).ROOT == root()


@pytest.mark.parametrize("name,relative", sorted(ROOMS.items()))
def test_room_never_counts_parent_directories(name, relative):
    """A fixed __file__ depth breaks asset resolution silently when a file moves."""
    source = (root()/relative).read_text(encoding="utf-8")
    assert not re.search(r"__file__\s*\)\s*\.resolve\(\)\.parents\[", source)


@pytest.mark.parametrize("name,relative", sorted(ROOMS.items()))
def test_room_assets_exist(name, relative):
    assets = getattr(load(name, relative), "ASSETS", None)
    assert assets is None or assets.is_dir()


def test_watchman_runs_without_the_course_package():
    """GitHub Actions runs watch.py with the standard library only; -S reproduces that."""
    result = subprocess.run([sys.executable, "-S", str(root()/ROOMS["watchman"]), "--help"],
                            capture_output=True, text=True, cwd=root())
    assert result.returncode == 0, result.stderr
    assert "usage: watch.py" in result.stdout
