from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Event:
    eventid: int
    eventname: str
    description: Optional[str]
    starttime: int
    endtime: int
    departmentid: int
    locationid: int
    categories: Optional[List[int]] = None
