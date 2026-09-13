"""Foundation verification test for Checkpoint 0."""

import os
from pathlib import Path

def test_workspace_structure():
    """Verify that all canonical project directories exist."""
    required_dirs = [
        "data/raw",
        "data/processed",
        "notebooks",
        "src/level0",
        "src/level1",
        "src/level2",
        "src/level3",
        "src/level4",
        "src/level5",
        "src/level6",
        "src/validation",
        "app",
        "outputs/charts",
        "outputs/tables",
        "outputs/reports",
        "screenshots/level1",
        "screenshots/level2",
        "screenshots/level3",
        "screenshots/level4",
        "screenshots/level5",
        "screenshots/level6",
        "documentation/level1",
        "documentation/level2",
        "documentation/level3",
        "documentation/level4",
        "documentation/level5",
        "documentation/level6",
        "tests",
    ]
    for rel_path in required_dirs:
        p = Path(rel_path)
        assert p.is_dir(), f"Directory missing: {rel_path}"

def test_raw_dataset_exists():
    """Verify that raw dataset exists in data/raw/Dataset1.csv and has content."""
    raw_path = Path("data/raw/Dataset1.csv")
    assert raw_path.is_file(), "data/raw/Dataset1.csv does not exist"
    assert raw_path.stat().st_size > 10_000_000, "data/raw/Dataset1.csv is smaller than expected"

def test_trackers_exist():
    """Verify task tracker and git checkpoint tracker exist."""
    assert Path("documentation/task_tracker.csv").is_file()
    assert Path("documentation/git_checkpoint_tracker.csv").is_file()
