from dataclasses import dataclass
from datetime import date

@dataclass
class Driver:
    driverId: int
    driverRef: str
    number: int
    code: str
    forename: str
    surname: str
    dob: date
    nationality: str
    url: str

    def __str__(self):
        return self.driverRef

    def __eq__(self, other):
        if isinstance(other, Driver):
            return self.driverId == other.driverId

    def __hash__(self):
        return hash(self.driverId)