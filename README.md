# Saint-Luc Bouges G6 - Upstream Prototypes

Prototype stack for the **Upstream** sub-problem:

> How might we better predict length of stay and improve communication with patients about their care pathway, to anticipate discharge earlier and more accurately?

## What this project includes

### 1) Interactive web demo (GitHub Pages)
- **File:** `index.html` (and `github-io/index.html`)
- **What it does:**
  - LOS forecast calculator
  - confidence estimation
  - early coordination flag
  - D-2 / D-1 / D0 communication preview
  - light/dark/auto theme + UI animations
  - Group 6 credentials footer

### 2) Forecast engine (Python)
- **File:** `los_forecast.py`
- **What it does:**
  - computes predicted LOS from patient attributes
  - computes confidence score/label
  - raises early coordination flag

### 3) Daily huddle board generator (Python)
- **File:** `daily_huddle_board.py`
- **Input:** `sample_patients.csv`
- **Output:** `out/daily_huddle_board.html`
- **What it does:**
  - creates a sortable operational board for discharge planning
  - prioritizes cases with lower confidence and stronger blockers

### 4) Communication flow generator (Python)
- **File:** `communication_flow.py`
- **Input:** `sample_patients.csv`
- **Output:** `out/patient_message_schedule.csv`
- **What it does:**
  - generates message schedule templates for D-2 / D-1 / D0

### 5) Publishing automation
- **File:** `publish_github_pages.sh`
- **What it does in one command:**
  1. creates/uses `.venv`
  2. regenerates Python outputs
  3. commits changes
  4. pushes to GitHub
  5. enables GitHub Pages (if needed)

## How the site works

The page runs fully in-browser (no backend).  
It reproduces the same rule logic as the Python forecast model:
- base LOS by procedure
- adjustments for age/comorbidity/social complexity/post-acute need
- confidence and early-coordination evaluation
- timeline communication triggers

## Quick start (Linux)

```bash
cd 6.Experiments/upstream-prototypes
python3 -m venv .venv
. .venv/bin/activate
python daily_huddle_board.py
python communication_flow.py
```

Open:
- `out/daily_huddle_board.html`
- `out/patient_message_schedule.csv`

## Publish / republish to GitHub Pages

```bash
cd 6.Experiments/upstream-prototypes
chmod +x publish_github_pages.sh
./publish_github_pages.sh Lord-Melflam saint-luc-bouges-g6-upstream-prototypes /
```

Expected URL:

`https://lord-melflam.github.io/saint-luc-bouges-g6-upstream-prototypes/`

## What to do with the Python code

Use Python as your **data/prototype backend**, and the web page as your **demo frontend**:

1. Keep editing `sample_patients.csv` to simulate realistic hospital cases.
2. Re-run Python scripts to regenerate board + message schedule artifacts.
3. Use generated outputs in your portfolio/slides as evidence of operational feasibility.
4. Publish updates with `publish_github_pages.sh` whenever you iterate.

In short: the Python files are not optional; they are your reproducible proof that the concept goes beyond slides.
