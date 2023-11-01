# yaml
from pathlib import Path
from typing import Literal
from typing_extensions import Annotated
from attr import dataclass
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
    mongo_uri: Annotated[str, "mongo_uri"]
    mongo_db: Annotated[str, "mongo_db"]
    mongo_collection: Annotated[str, "mongo_collection"]
    node_id: Annotated[str, "node_id"]


@dataclass
class NeuroPulseConfig:
    app_logging_level: Annotated[
        Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "app_logging_level"
    ]
    gpu_monitoring_interval: Annotated[int, "gpu_monitoring_interval"]
    handlers: Annotated[list[Handler], "gpu_monitoring_handlers"]
    environment_name: Annotated[str, "environment_name"]


def parse_configs(config_path: str):
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(str(config_path), "r") as f:
        config = yaml.safe_load(f)

    return NeuroPulseConfig(
        app_logging_level=config.get("app_logging_level", "INFO"),
        gpu_monitoring_interval=config.get("gpu_monitoring_interval", 5),
        handlers=[
            Handler.get_handler(handler["type"])(**handler.get("config", {}))
            for handler in config.get("handlers", [])
        ],
        environment_name=config.get("environment_name", "default"),
    )
