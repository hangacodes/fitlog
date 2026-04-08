from fitlog import parser
from fitlog.validators import workout_pipeline
from fitlog.validators import body_metrics_pipeline


records, rejects = parser.parse_file("data/body_metrics.csv", parser.parse_body_metric, parser.METRICS_TYPES, 6)
exercise_records, exercise_rejected = parser.parse_file("data/exercise_catalog.csv", parser.parse_exercise, parser.EXERCISE_TYPES, 4)
workouts_records, workouts_rejected = parser.parse_file("data/workouts.csv", parser.parse_workout, parser.WORKOUT_TYPES, 6)

catalog_names = {e.exercise_name.lower() for e in exercise_records}

valid_workouts, rejected_wouts = workout_pipeline(workouts_records, catalog_names)
valid_metrics , rejected_metrics = body_metrics_pipeline(records)

print(rejected_wouts.summary())
print(rejected_metrics.summary())

print(f"Valid workouts: {len(valid_workouts)} | Flagged: {rejected_wouts.total}")
print(f"Valid metrics: {len(valid_metrics)} | Flagged: {rejected_metrics.total}")