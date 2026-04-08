class InvalidFieldError(ValueError):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message  
        super().__init__(message)


class OutOfRangeError(ValueError):
    def __init__(self, field_name, actual_value, min_value, max_value):
        self.field_name = field_name
        self.value = actual_value
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(f"{field_name} value {actual_value} is out of range ({min_value} - {max_value})")


def validate_workout(record, catalog_names):
    workout_errors = []

    if not record.date:
        workout_errors.append("date is missing")
    if not record.exercise:
        workout_errors.append("exercise is missing")
    elif record.exercise.lower() not in catalog_names:
        workout_errors.append("exercise not found in catalog")
    if record.sets < 1 or record.sets > 10:
        workout_errors.append("unrealistic number of sets - must be between 1 - 10 sets")
    if record.reps < 1 or record.reps > 30:
        workout_errors.append("unrealistic number of reps - must be between 1 - 30 reps")
    if record.weight_kg <= 0:
        workout_errors.append("weight must be more than 0")
    if record.rpe is not None:
        if record.rpe < 1.0 or record.rpe > 10.0:
            workout_errors.append("rpe unrealistic - must be between 1.0 and 10.0")

    return workout_errors

def validate_metrics(record):
    body_metric_errors = []
   
    if not record.date:
        body_metric_errors.append("date is missing")
    if record.weight_kg < 30 or record.weight_kg > 200:
        body_metric_errors.append("weight is unrealistic - must be (30 - 200)")
    if record.sleep_hours < 0 or record.sleep_hours > 14:
        body_metric_errors.append("slept hours out of range - must be (0 - 14)")
    if record.calories < 500 or record.calories > 8000:
        body_metric_errors.append("calories are unrealistic - must be (500 - 8000)")
    if record.water_liters < 0 or record.water_liters > 10:
        body_metric_errors.append("liters of water out of range - must be (0 - 10)")
    if record.soreness < 1 or record.soreness > 10:
        body_metric_errors.append("soreness value out of range - must be (0 - 10)")

    return body_metric_errors


class ValidationReport:
    def __init__(self):
        self._issues = []

    def add_issue(self, record, errors, label):
        self._issues.append({ "record":record, "errors":errors, "label":label })

    @property
    def total(self):
        return len(self._issues)
    
    def summary(self):
        summary =[]
        summary.append(f"Total flagged records {self.total}")
        
        workout_count = 0
        body_metric_count = 0
        for issue in self._issues:
            if issue["label"] == "workout":
                workout_count += 1
            if issue["label"] == "body_metric":
                body_metric_count += 1
        summary.append(f"Workouts flagged: {workout_count}")
        summary.append(f"Body metrics flagged: {body_metric_count}")
        
        for issue in self._issues:
            summary.append(f"{issue['label']} : {issue['record'].date}")
            for error in issue["errors"]:
                summary.append(f"   - {error}")
        return "\n".join(summary)
    
def workout_pipeline(records , catalog_names):
    validated = []
    report = ValidationReport()
    for record in records:
        errors = validate_workout(record, catalog_names)
        if errors:
            report.add_issue(record, errors, "workout")
        else:
            validated.append(record)
    return validated, report

def body_metrics_pipeline(records):
    validated = []
    report = ValidationReport()

    for record in records:
        errors = validate_metrics(record)
        if errors:
            report.add_issue(record, errors, "body_metric")
        else:
            validated.append(record)
    
    return validated, report