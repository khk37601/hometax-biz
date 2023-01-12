import os

from dotenv import dotenv_values


class EnvironmentManager:
    def __init__(self, path=f'{os.getcwd()}/.env'):
        self.__config = {**dotenv_values(path)}

    def __del__(self):
        pass

    def get(self, name: str):
        return self.__config.get(name)
