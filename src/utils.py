import yaml
import os
from datetime import datetime


def load_config(path="config/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_versioned_path(base_dir: str, prefix: str, ext: str):
    os.makedirs(base_dir, exist_ok=True)
    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(base_dir, f"{prefix}_{version}.{ext}")


def get_latest_file(directory: str, prefix: str):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    files = [f for f in os.listdir(directory) if f.startswith(prefix)]
    if not files:
        raise FileNotFoundError(f"No files found with prefix '{prefix}' in {directory}")

    files.sort()
    return os.path.join(directory, files[-1])
