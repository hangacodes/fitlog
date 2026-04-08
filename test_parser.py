from fitlog import models
from fitlog import parser

metric_records, metric_rejects = parser.parse_file("data/body_metrics.csv", parser.parse_body_metric, parser.METRICS_TYPES, 6)
exercise_records, exercise_rejected = parser.parse_file("data/exercise_catalog.csv", parser.parse_exercise, parser.EXERCISE_TYPES, 4)
workouts_records, workouts_rejected = parser.parse_file("data/workouts.csv", parser.parse_workout, parser.WORKOUT_TYPES, 6)
print("Successfully parsed:\n")
for line in metric_records:
    print(f"metricsRecord:{line}")
for line in exercise_records:
    print(f"exercisesRecord:{line}")
for line in workouts_records:
    print(f"workoutsRecord:{line}")
print("Successfully Rejected:\n")
for line in metric_rejects:
    print(f"metricsRejected: {line}")
for line in exercise_rejected:
    print(f"exercisesRejected: {line}")    
for line in workouts_rejected:
    print(f"workoutsRejected: {line}")
print(workouts_records[0])