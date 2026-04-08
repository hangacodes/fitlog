def heavy_kg(workouts):
    '''Map each exercise with the heaviest weight_kg'''
    records = {}

    for record in workouts:
        if record.exercise not in records:
            records[record.exercise] = record.weight_kg
        else:
            if records[record.exercise] < record.weight_kg:
                records[record.exercise] = record.weight_kg
    return records
def count_volume(workouts):
    records = {}

    for record in workouts:
        volume = record.sets * record.reps * record.weight_kg
        if record.exercise not in records:
            records[record.exercise] = volume
        else:
            records[record.exercise] += volume

    return records

def workouts_freq(workouts):
    freq = {}

    for record in workouts:
        month = record.date[:7]
        if month not in freq:
            freq[month] = 1
        else:
            freq[month] += 1
    return freq


def metrics_avg(body_metrics):
    average = {}
    weight_total = 0
    sleep_total = 0
    calories_total = 0
    water_total = 0
    soreness_total = 0

    for record in body_metrics:
            weight_total += record.weight_kg
            sleep_total += record.sleep_hours
            calories_total += record.calories
            water_total += record.water_liters
            soreness_total += record.soreness
    average["Weight average"] = round(weight_total / len(body_metrics), 2)
    average["Sleep average"] = round(sleep_total / len(body_metrics), 2)
    average["Calories average"] = round(calories_total / len(body_metrics), 2)
    average["Water average"] = round(water_total / len(body_metrics), 2)
    average["Soreness average"] = round(soreness_total / len(body_metrics), 2)

    return average

def sleep_analytics(body_metrics):
    best_sleep = body_metrics[0]
    worst_sleep = body_metrics[0]

    for record in body_metrics:
        if record.sleep_hours > best_sleep.sleep_hours:
            best_sleep = record
        if record.sleep_hours < worst_sleep.sleep_hours:
            worst_sleep = record

    return best_sleep, worst_sleep


def soreness_sleep_extract(body_metrics):
    records = []
    for record in body_metrics:
        records.append({"date": record.date, "sleep_hours":record.sleep_hours, "soreness":record.soreness})

    def get_date(d):
        return d["date"]
    
    return sorted(records, key=get_date)