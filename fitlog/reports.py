import json
import pathlib


def write_quality_report(filepath, workout_rejects, metric_rejects,
                        workout_report, metric_report, total_workout_rows, total_metric_rows):
    with open(filepath, "w", encoding="utf-8") as f:
        valid_workouts , rejected_workouts = workout_report
        valid_metrics , rejected_metrics = metric_report

        f.write(f"Total workout rows: {total_workout_rows}\n")
        f.write(f"Total metric rows: {total_metric_rows}\n")
        f.write(f"Workouts rejected: {len(workout_rejects)}\n")
        f.write(f"Body metrics rejected: {len(metric_rejects)}\n")
        f.write(f"Rejected workouts at validation: {rejected_workouts.total}\n")
        f.write(f"Rejected metrics at validation: {rejected_metrics.total}\n")
        f.write("Rows that passed validation:\n")
        f.write(f"\t workouts rows: {len(valid_workouts)}\n")
        f.write(f"\t metrics rows: {len(valid_metrics)}\n")

        f.write("\n--- Parse Rejections ---\n")
        for line in workout_rejects:
            f.write(f"{line}\n")
        for line in metric_rejects:
            f.write(f"{line}\n")
        
        f.write("\n--- Validation Issues ---\n")
        f.write(rejected_workouts.summary())
        f.write("\n")
        f.write(rejected_metrics.summary())


def write_clean_workouts(filepath: str, valid_workouts:list):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("date,exercise,sets,reps,weight_kg,rpe,notes\n")
        for line in valid_workouts:
            date = line.date
            exercise = line.exercise
            sets = line.sets
            reps = line.reps
            weight_kg = line.weight_kg
            rpe = line.rpe
            notes = line.notes
            if notes is None:
                notes_str = ""
            elif "," in notes:
                notes_str = f'"{notes}"'
            else:
                notes_str = notes
            rpe_str = str(rpe) if rpe is not None else ""
            
            f.write(f"{date},{exercise},{sets},{reps},{weight_kg},{rpe_str},{notes_str}\n")

def write_summary_json(filepath, analytics_results:dict):
    with open(filepath, "w") as f:
        json.dump(analytics_results, f, indent=2)
