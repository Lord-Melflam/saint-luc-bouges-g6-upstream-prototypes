#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


PROCEDURE_BASE_LOS = {
    "orthopedic": 4.0,
    "digestive": 6.0,
    "urology": 5.0,
    "cardiovascular": 8.0,
    "general_surgery": 5.0,
    "emergency": 7.0,
}


@dataclass
class PatientCase:
    patient_id: str
    name: str
    procedure_type: str
    admission_date: date
    age: int
    comorbidity_score: int
    social_complexity: bool
    post_acute_need: bool
    blockers: str = ""


@dataclass
class ForecastResult:
    predicted_los_days: int
    confidence_score: float
    confidence_label: str
    expected_discharge_date: date
    early_coordination_flag: bool


def _base_los(procedure_type: str) -> float:
    return PROCEDURE_BASE_LOS.get(procedure_type, 5.5)


def forecast_los(case: PatientCase) -> ForecastResult:
    score = _base_los(case.procedure_type)

    if case.age >= 75:
        score += 1.0
    elif case.age >= 65:
        score += 0.5

    score += min(case.comorbidity_score * 0.6, 3.0)

    if case.social_complexity:
        score += 1.5
    if case.post_acute_need:
        score += 1.0
    if case.procedure_type == "emergency":
        score += 0.8

    predicted_los = max(1, round(score))

    confidence = 0.92
    confidence -= min(case.comorbidity_score * 0.08, 0.4)
    if case.social_complexity:
        confidence -= 0.12
    if case.post_acute_need:
        confidence -= 0.10
    if case.procedure_type == "emergency":
        confidence -= 0.08
    confidence = min(max(confidence, 0.35), 0.95)

    if confidence >= 0.75:
        label = "high"
    elif confidence >= 0.55:
        label = "medium"
    else:
        label = "low"

    expected_date = case.admission_date + timedelta(days=predicted_los)
    early_coordination = (
        label == "low"
        or case.social_complexity
        or case.post_acute_need
        or predicted_los >= 7
    )

    return ForecastResult(
        predicted_los_days=predicted_los,
        confidence_score=round(confidence, 2),
        confidence_label=label,
        expected_discharge_date=expected_date,
        early_coordination_flag=early_coordination,
    )
