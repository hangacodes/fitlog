from fitlog import parser
from fitlog import parser
from fitlog.validators import workout_pipeline
from fitlog.validators import body_metrics_pipeline
from fitlog import parser
from fitlog.validators import workout_pipeline
from fitlog.validators import body_metrics_pipeline
from fitlog.analytics import heavy_kg
from fitlog.analytics import count_volume
from fitlog import analytics
from fitlog.reports import write_clean_workouts, write_quality_report, write_summary_json


records, rejects = parser.parse_file("data/body_metrics.csv", parser.parse_body_metric, parser.METRICS_TYPES, 6)
exercise_records, exercise_rejected = parser.parse_file("data/exercise_catalog.csv", parser.parse_exercise, parser.EXERCISE_TYPES, 4)
workouts_records, workouts_rejected = parser.parse_file("data/workouts.csv", parser.parse_workout, parser.WORKOUT_TYPES, 6)

catalog_names = {e.exercise_name.lower() for e in exercise_records}

valid_workouts, rejected_wouts = workout_pipeline(workouts_records, catalog_names)
valid_metrics , rejected_metrics = body_metrics_pipeline(records)

personal_records = heavy_kg(valid_workouts)
volume_totals = count_volume(valid_workouts)
frequency = analytics.workouts_freq(valid_workouts)
averages = analytics.metrics_avg(valid_metrics)
result = analytics.soreness_sleep_extract(valid_metrics)
best_sleep, worst_sleep = analytics.sleep_analytics(valid_metrics)


analytics_results = {
    "personal_records": personal_records,
    "volume_totals": volume_totals,
    "averages": averages,
    "best_sleep": {"date": best_sleep.date, "sleep_hours": best_sleep.sleep_hours},
    "worst_sleep": {"date": worst_sleep.date, "sleep_hours": worst_sleep.sleep_hours},
    "workout_frequency": frequency
}
total_workout_rows = len(workouts_records) + len(workouts_rejected)
total_metrics_rows = len(records) + len(rejects)
write_quality_report("output/quality_report.txt", workouts_rejected, rejects, (valid_workouts, rejected_wouts), (valid_metrics, rejected_metrics), total_workout_rows, total_metrics_rows)
write_clean_workouts("output/clean_workouts.csv", valid_workouts)
write_summary_json("output/summary.json", analytics_results)