from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class SessionType(Enum):
    FP1 = "Free Practice 1"
    FP2 = "Free Practice 2"
    FP3 = "Free Practice 3"
    SPRINT_QUALIFYING = "Sprint Qualifying"
    SPRINT = "Sprint Race"
    QUALIFYING = "Qualifying"
    RACE = "RACE"

class WeekendType(Enum):
    STANDARD = "standard" #FP1, FP2, FP3, Quali, Race
    SPRINT = "sprint" #FP1, Sprint Quali, Sprint Race, Quali, Race


class TireCompound(Enum):
    SOFT = "Soft"
    MEDIUM = "Medium"
    HARD = "Hard"
    INTERMEDIATE = "Intermediate"
    WET = "Wet"

@dataclass
class TireAllocation:
    """
    Total amount of tire sets allowed as per FIA regulations
    """
    soft: int = 0
    medium: int = 0
    hard: int = 0
    intermediate: int = 4
    wet: int = 3

    def __post_init__(self):
        if self.soft == 0 and self.medium == 0 and self.hard == 0:
            self.soft = 8
            self.medium = 3
            self.hard = 2

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

    def use(self, laps: int, session: SessionType) -> None:
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

@dataclass
class SessionPlan:
    """
    Plan for a single given session
    """
    session_type = SessionType
    tire_sets_used: List[int]
    compounds_used = List[TireCompound]
    target_laps: int
    objective: List[str] #["long_run_data, "quali_sim", "setup_test"]

@dataclass
class WeekendStrategy:
    """
    Complete weekend strategy for all sessions
    """
    format: WeekendType
    session_plans: Dict[SessionType, SessionPlan]
    race_strategy: Dict[str, any] #plans A, B, C for race


class WeekendSim:
    """
    Simulated entire F1 weekend and optimizes
    """

    def __init__(self, track: str) -> None:
        self.track = track
        #self.format = format format: WeekendType, weather_forecast: Dict
        #self.weather_forecast = weather_forecast
        self.tire_allocation = TireAllocation()
        self.tire_inventory = self._initialize_tire_inventory()

    def _initialize_tire_inventory(self) -> List[TireSet]:
        """
        Create all available tire sets for the weekend
        """
        inventory = []
        set_num = 1

        for compound, count in [
            (TireCompound.SOFT, self.tire_allocation.soft),
            (TireCompound.MEDIUM, self.tire_allocation.medium),
            (TireCompound.HARD, self.tire_allocation.hard),
            (TireCompound.INTERMEDIATE, self.tire_allocation.intermediate),
            (TireCompound.WET, self.tire_allocation.wet)
        ]:
            for _ in range(count):
                inventory.append(TireSet(compound, set_num))
                set_num += 1

        return inventory

def main():
    tire = WeekendSim("Monza")
    print(tire.tire_inventory)

if __name__ == "__main__":
    main()