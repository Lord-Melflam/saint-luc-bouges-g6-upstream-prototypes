#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

from los_forecast import PatientCase, forecast_los


BASE_DIR = Path(__file__).resolve().parent
INPUT_CSV = BASE_DIR / "sample_patients.csv"
OUT_DIR = BASE_DIR / "out"
OUT_CSV = OUT_DIR / "patient_message_schedule.csv"


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


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


def _message_templates(name: str, expected: date) -> list[tuple[str, date, str]]:
    d2 = expected - timedelta(days=2)
    d1 = expected - timedelta(days=1)
    d0 = expected
    return [
        (
            "D-2",
            d2,
            f"Hello {name}, your current discharge target is around {expected.isoformat()}. "
            "Please prepare your home logistics and documents.",
        ),
        (
            "D-1",
            d1,
            f"Hello {name}, this is your D-1 update. Planned discharge remains {expected.isoformat()} "
            "unless your care team informs you otherwise.",
        ),
        (
            "D0",
            d0,
            f"Hello {name}, discharge day update: your care team will confirm the final departure time "
            "and your post-discharge instructions today.",
        ),
    ]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    for case in load_cases(INPUT_CSV):
        result = forecast_los(case)
        for stage, send_date, message in _message_templates(case.name, result.expected_discharge_date):
            rows.append(
                {
                    "patient_id": case.patient_id,
                    "patient_name": case.name,
                    "stage": stage,
                    "send_date": send_date.isoformat(),
                    "expected_discharge_date": result.expected_discharge_date.isoformat(),
                    "confidence_label": result.confidence_label,
                    "message_text": message,
                }
            )

    rows.sort(key=lambda r: (r["send_date"], r["patient_id"], r["stage"]))
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "patient_id",
                "patient_name",
                "stage",
                "send_date",
                "expected_discharge_date",
                "confidence_label",
                "message_text",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated: {OUT_CSV}")


if __name__ == "__main__":
    main()
