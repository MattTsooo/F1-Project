from dataclasses import dataclass
from typing import List
from enum import Enum

class SessionType(Enum):
    FP1 = "Free Practice 1"
    FP2 = "Free Practice 2"
    FP3 = "Free Practice 3"
    SPRINT_QUALIFYING = "Sprint Qualifying"
    SPRINT = "Sprint Race"
    QUALIFYING = "Qualifying"
    RACE = "RACE"

class TireCompound(Enum):
    SOFT = "Soft"
    MEDIUM = "Medium"
    HARD = "HARD"
    INTERMEDIATE = "Inter"
    WET = "Wet"

class TireAllocation:
    def __init__(self, soft, medium, hard):
        self.soft = soft
        self.medium = medium
        self.hard = hard

@dataclass
class TireSet:
    """
    Individual tire set's with usage tracking
    """
    compound: TireCompound
    set_number: int
    laps_used = int = 0
    sessions_used: List[SessionType] = None
    condition: float = 100.0

    def __post_init__(self):
        if self.sessions_used is None:
            self.sessions_used = []

    def use(self, laps: int, session: SessionType):
        """
        Update tire condition after usage
        """
        self.laps_used += laps
        if session not in self.sessions_used:
            self.sessions_used.append(session)

        deg_rate = {
            TireCompound.SOFT: 2.5,
            TireCompound.MEDIUM: 1.5,
            TireCompound.HARD: 1.0
        }

        self.condition -= deg_rate.get(self.compound, 1.5) * laps
        self.condition = max(0, self.condition)