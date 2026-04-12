'''Validation module — checks parsed records against business rules and range constraints.'''

'''Raised when a field contains an invalid value.'''
class InvalidFieldError(ValueError):
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message  
        super().__init__(message)


'''Raised when a numeric field falls outside its acceptable range.'''
class OutOfRangeError(ValueError):
    def __init__(self, field_name, actual_value, min_value, max_value):
        self.field_name = field_name
        self.value = actual_value
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(f"{field_name} value {actual_value} is out of range ({min_value} - {max_value})")


'''Check a WorkoutEntry against validation rules. Returns a list of error strings.'''
def validate_workout(record, catalog_names):
    workout_errors = []

    if not record.date:
        workout_errors.append("date field is missing")
    elif not record.date[:4].isdigit() or not record.date[5:7].isdigit() or not record.date[8:10].isdigit():
        workout_errors.append("date is not valid")
    if not record.exercise:
        workout_errors.append("exercise field is missing")
    elif record.exercise.lower() not in catalog_names:
        workout_errors.append("exercise not found in catalog")
    if not record.sets:
        workout_errors.append("sets field is missing")
    elif record.sets < 1 or record.sets > 10:
        workout_errors.append("unrealistic number of sets - must be between 1 - 10 sets")
    if not record.reps:
        workout_errors.append("reps field is missing")
    elif record.reps < 1 or record.reps > 30:
        workout_errors.append("unrealistic number of reps - must be between 1 - 30 reps")
    if not record.weight_kg:
        workout_errors.append("weight field is missing")
    elif record.weight_kg <= 0:
        workout_errors.append("weight must be more than 0")
    if record.rpe is not None:
        if record.rpe < 1.0 or record.rpe > 10.0:
            workout_errors.append("rpe unrealistic - must be between 1.0 and 10.0")

    return workout_errors


'''Check a BodyMetric against range constraints. Returns a list of error strings.'''
def validate_metrics(record):
    body_metric_errors = []
   
    if not record.date:
        body_metric_errors.append("date is missing")
    elif not record.date[:4].isdigit() or not record.date[5:7].isdigit() or not record.date[8:10].isdigit():
        body_metric_errors.append("date is not valid")
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


'''Collects validation issues across records and generates a text summary.'''
class ValidationReport:
    def __init__(self):
        self._issues = []

    '''Add a flagged record with its error list and category label.'''
    def add_issue(self, record, errors, label):
        self._issues.append({ "record":record, "errors":errors, "label":label })


    '''Return the total number of flagged records.'''
    @property
    def total(self):
        return len(self._issues)
    

    '''Return a formatted multi-line string of all validation issues.'''
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


'''Run validation on all parsed workouts. Returns (valid_records, ValidationReport).'''
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


'''Run validation on all parsed body metrics. Returns (valid_records, ValidationReport).'''
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