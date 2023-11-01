import time
from src.handlers.mongo_handler import MongoHandler
from src.common.logo import Logo
from src.monitors.gpu_monitor import GPUMonitoring
from src.app_logging.logger import create_logger
from src.configs.parse_configs import parse_configs
from src.app_logging.logger import logger


class App:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not App._instance:
            App._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return App._instance

    def start(self, config: str):
        logo = Logo()
        logo.show()
        pass


class NeuroImpulseApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.retry = 5
        self.retried = 0

    def start(self, config: str, node: str):
        self.configs = parse_configs(config)
        self.node = node
        self._start()

    def _start(self):
        super().start(self.configs)
        create_logger(level=self.configs.app_logging_level)
        logger.info("Starting NeuroPulse")

        for handler in self.configs.handlers:
            if isinstance(handler, MongoHandler):
                handler.node_id = self.node

        # start monitors
        gpu_monitor = GPUMonitoring(
            interval=self.configs.gpu_monitoring_interval,
            handlers=self.configs.handlers,
        )
        logger.info("Starting GPU monitoring")
        gpu_monitor.run()
        logger.info("GPU monitoring started")

        while True:
            if not gpu_monitor.is_alive():
                logger.error(
                    f"GPU monitoring process died. Restarting in {self.retried * 2} seconds"
                )
                if self.retried == self.retry:
                    logger.error(
                        f"GPU monitoring process died. Tried restarting {self.retry} times. Exiting"
                    )
                    exit(1)
                gpu_monitor.run()
                time.sleep(self.retried * 2)
                self.retried += 1

            time.sleep(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--node", type=str, required=True)
    args = parser.parse_args()

    app = NeuroImpulseApp()
    app.start(args.config)
