class SessionType:
    FP1 = "Free Practice 1"
    FP2 = "Free Practice 2"
    FP3 = "Free Practice 3"
    SPRINT_QUALIFYING = "Sprint Qualifying"
    SPRINT = "Sprint Race"
    QUALIFYING = "Qualifying"
    RACE = "RACE"

class TireCompound:
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

