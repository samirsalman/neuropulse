# yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from typing_extensions import Annotated
import yaml

from src.handlers.handler import Handler


@dataclass
class FileHandlerConfig:
    file_prefix: Annotated[str, "file_prefix"]
    rotate: Annotated[str, "rotate"]
    name: Annotated[str, "name"]
    mode: Annotated[Literal["append", "overwrite"], "mode"]
    gzip: Annotated[bool, "gzip"]


@dataclass
class MongoHandlerConfig:
    mongo_host: Annotated[str, "mongo_host"]
    mongo_collection: Annotated[str, "mongo_collection"]
    mongo_db: Annotated[str, "mongo_db"]
    node_id: Annotated[str, "node_id"]
    mongo_user: Annotated[str, "mongo_user"] = None
    mongo_password: Annotated[str, "mongo_password"] = None


@dataclass
class NeuroPulseConfig:
    app_logging_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "app_logging_level"
    ]
    gpu_monitoring_interval: Annotated[int, "gpu_monitoring_interval"]
    handlers: Annotated[list[Handler], "gpu_monitoring_handlers"]
    environment_name: Annotated[str, "environment_name"]


def parse_configs(config_path: str, node: str = None):
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(str(config_path), "r") as f:
        config = yaml.safe_load(f)

    environment_name = config.get("environment_name", "default")
    return NeuroPulseConfig(
        app_logging_level=config.get("app_logging_level", "INFO"),
        gpu_monitoring_interval=config.get("gpu_monitoring_interval", 5),
        environment_name=environment_name,
        handlers=[
            Handler.get_handler(handler["type"])(
                **handler.get("config", {}),
                node_id=node,
                mongo_collection=environment_name,
                mongo_db="neuropulse",
            )
            for handler in config.get("handlers", [])
        ],
    )
