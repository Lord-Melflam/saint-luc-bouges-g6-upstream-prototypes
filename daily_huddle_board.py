#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from los_forecast import PatientCase, forecast_los


BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "sample_patients.csv"
OUT_DIR = BASE_DIR / "out"
OUT_HTML = OUT_DIR / "daily_huddle_board.html"


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _priority_score(confidence: float, blockers: str, early_flag: bool) -> float:
    blocker_count = 0 if not blockers.strip() else len([b for b in blockers.split(";") if b.strip()])
    score = (1.0 - confidence) * 10 + blocker_count * 1.5
    if early_flag:
        score += 2
    return round(score, 2)


def load_cases(path: Path) -> list[PatientCase]:
    cases: list[PatientCase] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cases.append(
                PatientCase(
                    patient_id=row["patient_id"],
                    name=row["name"],
                    procedure_type=row["procedure_type"],
                    admission_date=date.fromisoformat(row["admission_date"]),
                    age=int(row["age"]),
                    comorbidity_score=int(row["comorbidity_score"]),
                    social_complexity=_to_bool(row["social_complexity"]),
                    post_acute_need=_to_bool(row["post_acute_need"]),
                    blockers=row.get("blockers", ""),
                )
            )
    return cases


def render_html(rows: list[dict[str, str]]) -> str:
    tr = []
    for row in rows:
        tr.append(
            "<tr>"
            f"<td>{row['patient_id']}</td>"
            f"<td>{row['name']}</td>"
            f"<td>{row['procedure_type']}</td>"
            f"<td>{row['predicted_los_days']}</td>"
            f"<td>{row['expected_discharge_date']}</td>"
            f"<td>{row['confidence_label']} ({row['confidence_score']})</td>"
            f"<td>{row['early_coordination_flag']}</td>"
            f"<td>{row['blockers']}</td>"
            f"<td>{row['priority_score']}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Upstream Daily Huddle Board</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f8fb; color: #1f2937; }}
    h1 {{ margin-bottom: 4px; }}
    p {{ margin-top: 0; color: #4b5563; }}
    table {{ border-collapse: collapse; width: 100%; background: white; }}
    th, td {{ border: 1px solid #e5e7eb; padding: 8px; font-size: 14px; }}
    th {{ background: #f3f4f6; text-align: left; }}
  </style>
</head>
<body>
  <h1>Upstream Daily Huddle Board</h1>
  <p>Generated from sample patients for Week 11 prototype.</p>
  <table>
    <thead>
      <tr>
        <th>ID</th><th>Name</th><th>Procedure</th><th>Pred LOS</th><th>Expected Discharge</th>
        <th>Confidence</th><th>Early Coordination</th><th>Blockers</th><th>Priority</th>
      </tr>
    </thead>
    <tbody>
      {''.join(tr)}
    </tbody>
  </table>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for case in load_cases(INPUT_CSV):
        result = forecast_los(case)
        rows.append(
            {
                "patient_id": case.patient_id,
                "name": case.name,
                "procedure_type": case.procedure_type,
                "predicted_los_days": str(result.predicted_los_days),
                "expected_discharge_date": result.expected_discharge_date.isoformat(),
                "confidence_label": result.confidence_label,
                "confidence_score": f"{result.confidence_score:.2f}",
                "early_coordination_flag": "yes" if result.early_coordination_flag else "no",
                "blockers": case.blockers or "-",
                "priority_score": f"{_priority_score(result.confidence_score, case.blockers, result.early_coordination_flag):.2f}",
            }
        )

    rows.sort(key=lambda r: float(r["priority_score"]), reverse=True)
    OUT_HTML.write_text(render_html(rows), encoding="utf-8")
    print(f"Generated: {OUT_HTML}")


if __name__ == "__main__":
    main()
