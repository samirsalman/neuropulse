from multiprocessing import Process
import subprocess
import time
from typing import List
from src.data.gpu_data import GPUData
from src.handlers.handler import Handler
from src.monitors.monitor import Monitor


class GPUMonitoring(Monitor):
    def __init__(self, interval: int = 5, handlers: List[Handler] = None) -> None:
        super().__init__(interval=interval)
        self.handlers = handlers
        if not self.handlers:
            self.handlers = []

    def _run(self):
        while True:
            out = subprocess.run(
                f"nvidia-smi --query-gpu=timestamp,index,gpu_bus_id,name,driver_version,fan.speed,temperature.gpu,power.draw,power.limit,memory.used,memory.total,utilization.gpu,utilization.memory --format=csv,noheader,nounits",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if out.returncode != 0:
                raise RuntimeError(
                    f"nvidia-smi returned with non-zero exit code: {out.returncode}"
                )
            gpu_usage = GPUData.from_csv_list(
                out.stdout.decode("utf-8").strip().splitlines()
            )

            for handler in self.handlers:
                handler.handle(gpu_usage)

            time.sleep(self.interval)

    def run(self):
        self.p = Process(target=self._run, daemon=True, name="gpu_monitor")
        self.p.start()

    def is_alive(self):
        return self.p.is_alive()

    def stop(self):
        self.p.terminate()
        self.p.join()
