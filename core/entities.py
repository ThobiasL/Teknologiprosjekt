from dataclasses import dataclass

@dataclass
class Alarm:
    hours: str = "00"
    minutes: str = "00"
    mode: int = 0
    state: str = "00:00:00"
    turned_on: bool = False
    timer: int = 0