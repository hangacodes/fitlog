# FitLog: Gym Data Pipeline

A Python data pipeline that reads raw gym workout and body metric CSV files, parses them with a hand-built CSV parser, validates every record against business rules, computes training analytics, and writes clean output files. Built without pandas or any external libraries — everything from CSV parsing to report generation is done from scratch using only the standard library.


## How to Run

Requires Python 3.10+.

```
python3 main.py
```

The pipeline prints parse and validation results to the terminal, then writes three output files to the `output/` directory: a data quality report, a clean workouts CSV, and a JSON analytics summary.


## Project Structure

```
fitlog/
├── data/
│   ├── workouts.csv           # Raw workout log (51 rows, includes dirty data)
│   ├── body_metrics.csv       # Raw daily body metrics (40 rows, includes dirty data)
│   └── exercise_catalog.csv   # Reference table of 12 exercises with muscle groups
├── fitlog/
│   ├── __init__.py            # Package marker
│   ├── models.py              # Dataclasses: WorkoutEntry, BodyMetric, ExerciseCatalogEntry
│   ├── parser.py              # CSV line splitting, type casting, file-level parsing
│   ├── validators.py          # Range checks, catalog lookups, ValidationReport class
│   ├── analytics.py           # Personal records, volume totals, averages, sleep stats
│   └── reports.py             # Writers for quality report, clean CSV, and JSON summary
├── output/
│   ├── main_quality_report.txt
│   ├── main_clean_workouts.csv
│   └── main_summary.json
├── main.py                    # Pipeline entry point — runs parse → validate → analyze → write
└── README.md
```


## Data Files

**workouts.csv** — 51 rows of workout sets with columns: `date`, `exercise`, `sets`, `reps`, `weight_kg`, `rpe`, `notes`. Intentionally includes dirty data: missing fields, non-numeric values (`heavy`), negative reps, exercises not in the catalog (`chest fly`), invalid dates (`not-a-date`), and rows with too few fields.

**body_metrics.csv** — 40 rows of daily body tracking with columns: `date`, `weight_kg`, `sleep_hours`, `calories`, `water_liters`, `soreness`. Dirty data includes: a missing date, a non-numeric calories value (`lots`), sleep hours of 25, negative weight, and whitespace-padded values.

**exercise_catalog.csv** — 12 exercises mapping `exercise_id`, `exercise_name`, `muscle_group`, and `equipment`. Used as a lookup table during validation.


## Output Files

**quality_report.txt** — Summarizes how many rows were parsed vs. rejected at the parsing stage, how many failed validation, and lists every rejected row with its specific error.

**clean_workouts.csv** — Contains only the 42 workout rows that passed both parsing and validation. Ready for downstream analysis.

**summary.json** — Analytics results including personal records (heaviest weight per exercise), total volume per exercise, body metric averages, best/worst sleep days, and workout frequency by month.


## Sample Output

Terminal output from `python3 main.py`:

```
FitLog Pipeline - Starting...

---Parse results---

body_metrics.csv:
- parsed: 39 rows
- rejected: 1 rows

workouts.csv:
- parsed: 49 rows
-rejected: 2 rows

exercise_catalog.csv:
- parsed: 12 rows
-rejected: 0 rows

---Validation results---

Workouts -> valid: 42 | flagged: 7
Metrics -> valid: 36 | flagged: 3

---Pipeline Completed---

---Files written---
Quality report -> output/quality_report.txt
Clean workouts -> output/clean_workouts.csv
JSON summary -> output/summary.json
```

Excerpt from `quality_report.txt`:

```
Total workout rows: 51
Total metric rows: 40
Workouts rejected: 2
Body metrics rejected: 1
Rejected workouts at validation: 7
Rejected metrics at validation: 3
Rows that passed validation:
	 workouts rows: 42
	 metrics rows: 36

--- Parse Rejections ---
Line:47 - Error Line doesn't have enough fields to be parsed: 2026-02-07,barbell row,4,8,57.5
Line:48 - Error field 4 could not be cast: 2026-02-09,squat,4,8,heavy,8.0,
Line:16 - Error field 3 could not be cast: 2026-01-20,81.5,7.5,lots,2.5,4 
```


## What I Learned

- **Manual CSV parsing**: Built a character-by-character CSV parser that handles quoted fields with commas, instead of using Python's `csv` module.
- **Two-stage data cleaning**: Separating parsing (can the row be read at all?) from validation (does the data make sense?) catches different classes of errors and keeps the logic modular.
- **Dataclasses for structured records**: Used `@dataclass` to define typed data containers, making the pipeline's data flow explicit and readable.
- **Accumulator pattern**: Every analytics function follows the same shape — initialize a container, loop through records, build up results. Recognizing this pattern made writing new analytics functions faster.
- **File I/O and project structure**: Organized code into a proper Python package with separate modules for each pipeline stage, reading from `data/` and writing to `output/`.