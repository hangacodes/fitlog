from dataclasses import dataclass

@dataclass
class WorkoutEntry:
    date : str
    exercise : str
    sets : int
    reps : int
    weight_kg: float
    rpe : float
    notes : str
@dataclass
class BodyMetric:
    date: str
    weight_kg: float
    sleep_hours: float
    calories: int
    water_liters: float
    soreness: int
@dataclass
class ExerciseCatalogEntry:
    exercise_id: str
    exercise_name: str
    muscle_group: str
    equipment: str


    