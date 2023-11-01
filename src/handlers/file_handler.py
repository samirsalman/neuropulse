import enum
from pathlib import Path
import re
import tarfile
from typing import List
from src.data.generic_data import GenericData
from src.handlers.handler import Handler, HandlerMode
from src.app_logging.logger import logger
from src.data.gpu_data import GPUData


class RotateStrategy(enum.Enum):
    DAILY = 1
    WEEKLY = 7
    MONTHLY = 30
    SIZE = 0


def validate_rotate(rotate: str) -> (RotateStrategy, int):
    # check if is size format or range format
    try:
        rotate = int(rotate)
        if rotate <= 0:
            raise ValueError
        return RotateStrategy.SIZE, rotate
    except ValueError:
        pass

    if rotate in ["daily", "weekly", "monthly"]:
        strategy = RotateStrategy(rotate.upper())
        rotate_interval = strategy.value
        return strategy, rotate_interval

    else:
        raise ValueError(
            f"Invalid rotate value: {rotate}. Must be in ['daily', 'weekly', 'monthly'] or a size in bytes"
        )


class FileHandler(Handler):
    def __init__(
        self,
        file_prefix: str = "file_handler.log",
        rotate: str = None,
        name: str = None,
        mode: HandlerMode = HandlerMode.APPEND,
        gzip: bool = False,
    ) -> None:
        super().__init__(name, mode)
        self.file_prefix = file_prefix
        self.rotate = rotate
        if self.rotate:
            self.rotate_strategy, self.rotate_interval = validate_rotate(rotate)
        self.gzip = gzip
        self.file = Path("/var/log/.neuropulse", "logs") / (self.file_prefix + ".log")
        self.file.parent.mkdir(parents=True, exist_ok=True)

        self.last_index = 0
        if self.file.exists():
            with open(str(self.file), "r") as f:
                for _ in f:
                    self.last_index += 1
        else:
            self.file.touch()
            with open(str(self.file), "w") as f:
                f.write(GPUData.get_header() + "\n")

        self.rotate_file()

    def compress(self, new_file: Path, next_log_index: int):
        if self.gzip:
            with tarfile.open(
                str(f"{self.file}.{next_log_index}.tar.gz"), "w:gz"
            ) as tar:
                tar.add(new_file, arcname=new_file.name)
            self.clear()
            new_file.unlink()
            logger.info(f"Compressing file {new_file}")

    def get_next_log_index(self):
        last = 0
        for file in self.file.parent.glob(f"{self.file.name}.*"):
            if re.match(f"{self.file.name}.[0-9]+", file.name):
                if file.suffix == ".gz":
                    last = max(last, int(file.name.split(".")[-3]))
                else:
                    last = max(last, int(file.name.split(".")[-1]))
        return last + 1

    def rotate_file(self):
        next_log_index = self.get_next_log_index()
        if self.rotate_strategy == RotateStrategy.SIZE:
            if self.file.stat().st_size > self.rotate_interval:
                new_file = self.file.rename(
                    self.file.parent / f"{self.file.name}.{next_log_index}"
                )
                self.last_index = 0
                logger.info(f"Rotating file {self.file} to {new_file}")

                self.compress(new_file, next_log_index)

    def handle(self, data: List[GenericData]):
        if not self.file.exists():
            with open(str(self.file), "w") as f:
                f.write(data[0].get_header() + "\n")
            self.last_index += 1
        with open(str(self.file), "a") as f:
            for d in data:
                f.write(d.to_csv() + "\n")
        self.last_index += 1
        self.rotate_file()

    def clear(self):
        if self.file.exists():
            open(str(self.file), "w").close()
        self.last_index = 0

    def get_last(self):
        return self.get_index(self.last_index)

    def get_all(self):
        return self.get_last_n(self.last_index)

    def get_last_n(self, n: int):
        if n > self.last_index:
            logger.warn(
                f"Cannot get the last {n} lines because there are only {self.last_index} lines in the file"
            )
            n = self.last_index
        return self.get_index(self.last_index - n)

    def get_index(self, index: int):
        if index > self.last_index:
            logger.warn(
                f"Cannot get the line {index} because there are only {self.last_index} lines in the file"
            )
            return None
        with open(str(self.file), "r") as f:
            for _ in range(index):
                f.readline()
            return f.readline().strip()
