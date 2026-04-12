from fitlog.parser import parse_body_metric, parse_exercise, parse_file, parse_workout, METRICS_TYPES, WORKOUT_TYPES, EXERCISE_TYPES
from fitlog.validators import workout_pipeline, body_metrics_pipeline
from fitlog.analytics import heavy_kg, count_volume, sleep_analytics, metrics_avg, soreness_sleep_extract, workouts_freq
from fitlog.reports import write_clean_workouts, write_quality_report, write_summary_json

def run_pipeline():
    print("FitLog Pipeline - Starting...\n")
    try:
        #--- Parsing the files into parsed and rejected ---
        parsed_metrics, metric_not_parseble = parse_file("data/body_metrics.csv", parse_body_metric, METRICS_TYPES, 6)
        parsed_catalog, catalog_not_parseble = parse_file("data/exercise_catalog.csv", parse_exercise, EXERCISE_TYPES, 4)
        parsed_workouts, workouts_not_parseble = parse_file("data/workouts.csv", parse_workout, WORKOUT_TYPES, 6)

        #--- catalog_names used for validation ---
        catalog_names = {e.exercise_name.lower() for e in parsed_catalog}

        #--- validating the parsed files ---
        valid_workouts, rejected_workouts = workout_pipeline(parsed_workouts, catalog_names)
        valid_metrics , rejected_metrics = body_metrics_pipeline(parsed_metrics)


        #---analytics---
        personal_records = heavy_kg(valid_workouts)      
        volume_totals = count_volume(valid_workouts)       
        frequency = workouts_freq(valid_workouts)       
        averages = metrics_avg(valid_metrics)      
        best_sleep, worst_sleep = sleep_analytics(valid_metrics)
        best_sleep, worst_sleep = sleep_analytics(valid_metrics)

        analytics_results = {
            "personal_records": personal_records,
            "volume_totals": volume_totals,
            "averages": averages,
            "workout_frequency": frequency
            }

        if best_sleep and worst_sleep:
            analytics_results["best_sleep"] = {"date": best_sleep.date, "sleep_hours": best_sleep.sleep_hours}
            analytics_results["worst_sleep"] = {"date": worst_sleep.date, "sleep_hours": worst_sleep.sleep_hours}
        total_workout_rows = len(parsed_workouts) + len(workouts_not_parseble)
        total_metrics_rows = len(parsed_metrics) + len(metric_not_parseble)
        #---output files---
        quality_report_path = "output/quality_report.txt"
        clean_workouts_path = "output/clean_workouts.csv"
        json_summary_path = "output/summary.json"

        write_quality_report(quality_report_path, workouts_not_parseble, metric_not_parseble, (valid_workouts, rejected_workouts), (valid_metrics, rejected_metrics), total_workout_rows, total_metrics_rows)
        write_clean_workouts(clean_workouts_path, valid_workouts)
        write_summary_json(json_summary_path, analytics_results)

        #--- OUTPUT ---
        
        print("---Parse results---\n")
        print(f"body_metrics.csv:")
        print(f"- parsed: {len(parsed_metrics)} rows")
        print(f"- rejected: {len(metric_not_parseble)} rows")
        print(f"\nworkouts.csv:")
        print(f"- parsed: {len(parsed_workouts)} rows")
        print(f"-rejected: {len(workouts_not_parseble)} rows")
        print(f"\nexercise_catalog.csv:")
        print(f"- parsed: {len(parsed_catalog)} rows")
        print(f"-rejected: {len(catalog_not_parseble)} rows")

        print("\n---Validation results---\n")
        print(f"Workouts -> valid: {len(valid_workouts)} | flagged: {rejected_workouts.total} ")
        print(f"Metrics -> valid: {len(valid_metrics)} | flagged: {rejected_metrics.total}")

        print(f"\n---Pipeline Completed---\n")
        print(f"---Files written---")
        print(f"Quality report -> {quality_report_path}")
        print(f"Clean workouts -> {clean_workouts_path}")
        print(f"JSON summary -> {json_summary_path}")
    except FileNotFoundError as e:
        print(f"Missing file: {e}")
    except PermissionError as e:
        print(f"Pipeline failed: {e}")
    except Exception as e:
        print(f"Something unexpected happened: {e}")


if __name__ == "__main__":
    run_pipeline()

