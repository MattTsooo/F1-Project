from tyre_organizer import WeekendType, TireCompound, TireSet, TireAllocation, SessionType, SessionPlan
from typing import Dict, List

class WeekendSim:
    """
    Simulated entire F1 weekend and optimizes
    """

    def __init__(self, track: str, format: WeekendType, weather_forecast: Dict) -> None:
        self.track = track
        self.format = format
        self.weather_forecast = weather_forecast
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

    def plan_practice_sessions(self) -> Dict[SessionType, SessionPlan]:
        """
        Plan FP1, FP2, FP3 with objectives:
        - Initial Setup (FP1)
        - Long run data collection (FP2)
        - Quali simulation + final setup (FP3)
        """

        plans = {}

        if self.format == WeekendType.STANDARD:
            #FP1
            plans[SessionType.FP1] = SessionPlan(
                session_type = SessionType.FP1,
                tire_sets_used = [11,12], #HARD x2
                compounds_used = [TireCompound.HARD, TireCompound.HARD],
                target_laps = 25,
                objectives = ["aero_balance", "mechanical_setup", "baseline_times"]
            )

            plans[SessionType.FP1] = SessionPlan(
                session_type=SessionType.FP2,
                tire_sets_used=[9, 10, 4],  #MEDIUM x2, SOFT x1
                compounds_used=[TireCompound.MEDIUM, TireCompound.MEDIUM, TireCompound.SOFT],
                target_laps=35,
                objectives=["race_pace", "tire_deg_data", "fuel_load_testing"]
            )

            plans[SessionType.FP3] = SessionPlan(
                session_type=SessionType.FP3,
                tire_sets_used=[1, 2],  #SOFT x2
                compounds_used=[TireCompound.SOFT, TireCompound.SOFT],
                target_laps=20,
                objectives=["quali_sim", "final_setup", "low_fuel_pace"]
            )

        elif self.format == WeekendType.SPRINT:
            plans[SessionType.FP1] = SessionPlan(
                session_type=SessionType.FP1,
                tire_sets_used=[11, 12, 3, 4],  #HARD x2, SOFT x2
                compounds_used=[TireCompound.HARD, TireCompound.HARD, TireCompound.SOFT, TireCompound.SOFT],
                target_laps=30,
                objectives=["full_setup", "quali_prep", "sprint_race_sim"]
            )

        return plans

    def plan_qualifying(self, session: SessionType):
        """
        Plan (Sprint) Qualifying tire usage
        Q1: 7 min, Q2: 10 min, Q3: 12 min
        """

        if session == SessionType.QUALIFYING:
            return SessionPlan(
                session_type=SessionType.QUALIFYING,
                tire_sets_used=[5, 6, 7, 8],  #SOFT x4
                compounds_used=[TireCompound.SOFT] * 4,
                target_laps=12,
                objectives=[
                    "Q1: 1 set for safety (Set 5)",
                    "Q2: 1-2 sets to reach Q3 (Sets 6, 7)",
                    "Q3: Best available sets (Set 8)"
                ]
            )
        else:
            return SessionPlan(
                session_type=SessionType.SPRINT_QUALIFYING,
                tire_sets_used=[1, 2, 5],  #SOFT x3
                compounds_used=[TireCompound.SOFT] * 3,
                target_laps=9,
                objectives=[
                    "SQ1: 1 set",
                    "SQ2: 1 set",
                    "SQ3: 1 fresh set"
                ]
            )

    def plan_sprint_race(self):
        """
        PLan sprint race
        Starting tire used is whatever tire that was used for qualifying (must use for 2 laps)
        """
        return SessionPlan(
            session_type=SessionType.SPRINT,
            tire_sets_used=[2],
            compounds_used=[TireCompound.SOFT],
            target_laps=17,
            objectives=["score_points", "gather_race_data", "minimize_risk"]
        )

    def optimize_race_strategy(self, available_tires: List[TireSet]) -> Dict:
        """
        Generate Plans A, B, C for the race using remaining tires
        Must use 2 different compounds as per FIA regulations
        """
        good_tires = [t for t in available_tires if t.condition > 70]
        old_tires = [t for t in available_tires if 30 < t.condition <= 70]

        strategies = {
            'plan_a': {
                'name': 'One-Stop: Medium → Hard',
                'stints': [
                    {
                        'compound': TireCompound.MEDIUM,
                        'tire_set': [t for t in good_tires if t.compound == TireCompound.MEDIUM][0].set_number,
                        'laps': 30,
                        'starting_condition': 100.0
                    },
                    {
                        'compound': TireCompound.HARD,
                        'tire_set': [t for t in good_tires if t.compound == TireCompound.HARD][0].set_number,
                        'laps':23,
                        'starting condition': 100.0
                    }
                ],
                'pit_laps': [30],
                'predicted_laps': 542
            }
        }