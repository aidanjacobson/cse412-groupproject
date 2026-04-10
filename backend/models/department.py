from dataclasses import dataclass
from typing import Optional


@dataclass
class Department:
    departmentid: int
    name: str
    contactemail: str
    phonenumber: Optional[str] = None
    website: Optional[str] = None
