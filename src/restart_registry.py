from src.utils.singleton import Singleton


class RestartRegistry(metaclass=Singleton):
    def __init__(self):
        self.restarted = False

    def set_restart_state(self, restarted: bool):
        self.restarted = restarted
