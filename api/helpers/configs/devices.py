import yaml
import requests
import os

from loguru import logger
from apscheduler.schedulers.background import BackgroundScheduler


class DevicesConfig:
    def __init__(self, devices_url):
        self.__DEVICES_URL = devices_url
        self.scheduler = BackgroundScheduler(daemon=True)
        self.init_file()
        self.update_yaml()

    def init_file(self):
        try:
            response = requests.get(self.__DEVICES_URL)
            yaml_file = os.path.basename(self.__DEVICES_URL)
            with open(yaml_file, "wb") as file:
                file.write(response.content)

            logger.info(f"Successfully download {yaml_file}")
            with open(yaml_file, "r") as config_file:
                self.config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

        except Exception as e:  # TODO: Add exceptions
            logger.error(e)

    def get(self, name: str) -> dict:
        return self.config.get(name, None)

    def set_device(self, name: str, data: dict):
        self.config[name] = data

    def save_file(self):
        with open(self.filename, "w") as config_file:
            config_file.write(yaml.dump(self.config))

    def update_yaml(self):
        self.scheduler.add_job(lambda: self.init_file(), "interval", seconds=3600)
        self.scheduler.start()
