from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Event:
    eventid: int
    eventname: str
    description: Optional[str]
    starttime: datetime
    endtime: datetime
    departmentid: int
    locationid: int
    categories: Optional[List[int]] = None
