# Saint-Luc Bouges G6 — Upstream Prototypes

Prototype stack for the **Upstream** sub-problem:

> How might we better predict LOS and improve discharge coordination early enough to reduce bed-flow friction while preserving care continuity?

## Current web prototype (3 pages)

### 1) Forecast & Coordination (`index.html`)
- Severity-based forecasting inputs (`severityType`, `severityScore`)  
- Automatic mapping: `procedure type -> service + specialty`
- Patient creation/update flow with explicit IDs
- Billing-threshold risk (default threshold: `12:00`)
- Communication outputs (nurse script + SMS timeline)
- Role modes:
  - planner (full panel)
  - nurse (lighter view)
- Scenario presets:
  - late transport
  - unresolved blocker
  - late medical validation
  - occupancy spike
  - missing critical data

### 2) Operations Matrix (`operations.html`)
- Service/chamber/bed occupancy matrix
- Global view + per-service filtering
- Bed drilldown with patient details
- Bed lifecycle actions:
  - assign waiting patient to free bed
  - discharge occupied bed (frees bed instantly)
- "Modify patient in Forecast page" handoff to edit flow

### 3) Tutorial (`tutorial.html`)
- Feature explanation and page-by-page guidance
- Role explanation
- Suggested demo flow for stakeholder presentations

## Shared state model

The web prototype runs client-side and stores synchronized state in browser storage (`localStorage`):
- key: `upstream-shared-state-v1`
- shared across Forecast + Operations pages
- includes patient registry and bed occupancy

This means actions on one page are reflected on the other page without backend.

## Python artifacts (supporting evidence)

### Forecast engine
- `los_forecast.py`

### Daily huddle board generator
- `daily_huddle_board.py`
- input: `sample_patients.csv`
- output: `out/daily_huddle_board.html`

### Communication flow generator
- `communication_flow.py`
- input: `sample_patients.csv`
- output: `out/patient_message_schedule.csv`

## Quick start (Linux)

```bash
cd 6.Experiments/upstream-prototypes
python3 -m venv .venv
. .venv/bin/activate
python daily_huddle_board.py
python communication_flow.py
```

Open generated artifacts:
- `out/daily_huddle_board.html`
- `out/patient_message_schedule.csv`

## Publish / republish to GitHub Pages

```bash
cd 6.Experiments/upstream-prototypes
chmod +x publish_github_pages.sh
./publish_github_pages.sh Lord-Melflam saint-luc-bouges-g6-upstream-prototypes / "Your commit message"
```

Live URL:

`https://lord-melflam.github.io/saint-luc-bouges-g6-upstream-prototypes/`

## Workflow note for edits

When a patient is opened from Operations for modification:
- Forecast page enters edit mode (`?editPatient=...`)
- user can:
  - confirm update
  - decline update
  - optionally recompute LOS

This supports operations-driven updates without forcing forecast recomputation every time.
