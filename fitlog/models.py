'''Data models for FitLog pipeline records.'''
from dataclasses import dataclass


'''A single workout set entry parsed from the workouts CSV.'''
@dataclass
class WorkoutEntry:
    date : str
    exercise : str
    sets : int
    reps : int
    weight_kg: float
    rpe : float
    notes : str

'''A single day's body metrics parsed from the body_metrics CSV.'''
@dataclass
class BodyMetric:
    date: str
    weight_kg: float
    sleep_hours: float
    calories: int
    water_liters: float
    soreness: int

'''A reference entry mapping exercise names to muscle groups and equipment.'''
@dataclass
class ExerciseCatalogEntry:
    exercise_id: str
    exercise_name: str
    muscle_group: str
    equipment: str


    