#This is a throwaway script - it won't be part of the final pipeline.

from pathlib import Path


p1= Path("data") / "body_metrics.csv"
p2= Path("data") / "exercise_catalog.csv"
p3= Path("data") / "workouts.csv"
paths = [p1, p2, p3]
for path in paths:

    print(f"File name: {path.name}\n")
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()
        header_parts = header.split(",")
        row_counts = 0
        raw_lines = []
        bad_rows = []
        for line in f:
            raw_lines.append(line)
            row_counts += 1
            parts = line.split(",")
            if len(parts) != len(header_parts):
                bad_rows.append(f"Line {row_counts} incomplete:{line}")
        for i in range(0,3):
            print(f"Line {i+1}: {raw_lines[i]}")
        for i in range(-2,0):
            print(f"Line {len(raw_lines) + i + 1}: {raw_lines[i]}")
    
        for row in bad_rows:
            print(row)
       