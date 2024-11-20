from abc import ABC, abstractmethod
from typing import Dict, List

class DatabasePort(ABC):
    @abstractmethod
    def send_auto_door_lock_time(self, status: int):
        pass

    @abstractmethod
    def read_variable_status(self):
        pass

    @abstractmethod
    def read_auto_door_lock_time(self) -> str:
        pass

    @abstractmethod
    def read_medication_doses(self, day: str) -> Dict[str, bool]:
        pass

    @abstractmethod
    def send_medication_dose_status(self, medication_id: int, dose_id: int):
        pass

    @abstractmethod
    def read_tasks(self) -> List[Dict]:
        pass

    @abstractmethod
    def task_done(self, task_name: str, task_time: str):
        pass