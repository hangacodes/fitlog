from fitlog import models
WORKOUT_TYPES = [str, str, int, int, float, float, str]
METRICS_TYPES = [str, float, float, int, float, int]
EXERCISE_TYPES = [str, str, str, str]
def csv_line_parser(line, delimiter = ","):
    fields = []
    current = ""
    in_quotes = False
 
    i = 0
    while i < len(line):
        ch = line[i]

        if ch == '"':
            in_quotes = not in_quotes
        elif ch == delimiter and not in_quotes:
            fields.append(current)
            current = ""
        else:
            current += ch

        i += 1

    fields.append(current)
    return fields
    

def cast_fields(fields, types):
    result = []
    for i in range(len(fields)):
        if fields[i] == "":
            result.append(None)
        else:
            try:
                result.append(types[i](fields[i]))
            except ValueError:
                raise ValueError(f"field {i} could not be cast")
    return result


def parse_workout(fields):
    return models.WorkoutEntry(
        date = fields[0],
        exercise = fields[1],
        sets = fields[2],
        reps = fields[3],
        weight_kg = fields[4],
        rpe = fields[5] if len(fields) > 5 else None,
        notes = fields[6] if len(fields) > 6 else None
    )
def parse_body_metric(fields):
    return models.BodyMetric(
        date = fields[0],
        weight_kg = fields[1],
        sleep_hours = fields[2],
        calories = fields[3],
        water_liters = fields[4],
        soreness = fields[5]
    )

def parse_exercise(fields):
    return models.ExerciseCatalogEntry(
        exercise_id = fields[0],
        exercise_name = fields[1],
        muscle_group = fields[2],
        equipment = fields[3]
    )


def parse_file(path, parse_fn, types, min_fields):
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()
        line_count = 0
        records = []
        rejected_records = []
        for line in f:
            line_count += 1
            line = line.strip("\n")
            try:
                fields = csv_line_parser(line)
                if not len(fields) >= min_fields:
                    raise ValueError("Line doesn't have enough fields to be parsed")
                
                result = cast_fields(fields, types)
                records.append(parse_fn(result))
                

                
            except ValueError as e:
                rejected_records.append(f"Line:{line_count} - Error {e}: {line} ")
            
        return records, rejected_records