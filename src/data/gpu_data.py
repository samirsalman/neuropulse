from dataclasses import dataclass
from src.data.generic_data import GenericData
from src.app_logging.logger import logger


@dataclass
class GPUData(GenericData):
    timestamp: str
    index: int
    pci_bus_id: str
    name: str
    driver_version: str
    fan_speed: float
    temperature: float
    power_draw: float
    power_limit: float
    memory_used: float
    memory_total: float
    utilization_gpu: float
    utilization_memory: float

    @staticmethod
    def get_header():
        return "timestamp,index,pci.bus_id,name,driver_version,fan.speed [%],temperature.gpu,power.draw [W],power.limit [W],memory.used [MiB],memory.total [MiB],utilization.gpu [%],utilization.memory [%]"

    def to_csv(self):
        return f"{self.timestamp},{self.index},{self.pci_bus_id},{self.name},{self.driver_version},{self.fan_speed},{self.temperature},{self.power_draw},{self.power_limit},{self.memory_used},{self.memory_total},{self.utilization_gpu},{self.utilization_memory}"

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "index": self.index,
            "pci_bus_id": self.pci_bus_id,
            "name": self.name,
            "driver_version": self.driver_version,
            "fan_speed": self.fan_speed,
            "temperature": self.temperature,
            "power_draw": self.power_draw,
            "power_limit": self.power_limit,
            "memory_used": self.memory_used,
            "memory_total": self.memory_total,
            "utilization_gpu": self.utilization_gpu,
            "utilization_memory": self.utilization_memory,
        }

    @classmethod
    def from_csv(cls, csv: str):
        if len(csv.split(",")) != 13:
            logger.warn(
                f"Cannot parse the following line because it does not have 13 columns: {csv}"
            )
            return None
        return cls(*csv.split(","))

    @classmethod
    def from_json(cls, json: dict):
        return cls(**json)

    @classmethod
    def from_dict(cls, dict: dict):
        return cls(**dict)

    @classmethod
    def from_csv_list(cls, csv_list: list):
        return [cls.from_csv(csv) for csv in csv_list]

    @classmethod
    def from_json_list(cls, json_list: list):
        return [cls.from_json(json) for json in json_list]
