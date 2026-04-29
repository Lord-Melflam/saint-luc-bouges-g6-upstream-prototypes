# Upstream Prototypes Roadmap

## Goal
Turn the current upstream demo into a pilot-oriented discharge coordination tool aligned with stakeholder feedback and the project core problem (discharge optimization with care continuity).

## Phase 0 — Scope freeze
- Confirm one pilot unit + one specialty pathway as default scenario.
- Confirm v1 KPIs and alert ownership rules.
- Keep out-of-scope items explicit (infra expansion, full downstream redesign).

## Phase 1 — Core data and state foundation
- Define a shared patient data contract:
  - identity/context, unit/service, specialty, procedure type/subtype
  - expected discharge date, confidence, blockers
  - billing-threshold fields (`discharge_threshold_time`, risk status)
- Implement a single source of truth (shared state model).
- Ensure all UI sections consume the same state (synchronized updates).

## Phase 2 — Operational dashboard (control tower)
- Add occupancy-by-service view.
- Add discharge pipeline view (D-2 / D-1 / D0).
- Add threshold-risk panel (before/after 12:00 exposure).
- Add blocker distribution and urgent case queue.

## Phase 3 — Decision support and alerts
- Implement threshold warning levels (info / warning / critical).
- Map alerts to ownership roles (planner/coordinator primary).
- Add missing/uncertain data warnings (safety-first behavior).

## Phase 4 — Scenario simulation
- Provide preset scenarios:
  - late transport
  - unresolved blocker
  - late medical validation
  - occupancy spike
  - missing critical data
- Show expected impact deltas on KPIs per scenario.

## Phase 5 — Role-based UX and tutorial
- Add profile-based modes (planning-heavy vs light clinical view).
- Add in-app tutorial section:
  - how to read dashboard
  - how to process alerts
  - how to run simulation scenarios for presentation/demo

## Phase 6 — Evidence and portfolio alignment
- Align site narrative with implemented features (feature -> decision -> impact).
- Keep annex/deliverable pointers synchronized with demonstrated behavior.

## Current next step
Start Phase 1 with concrete schema and shared state implementation plan.

## Progress log
- [x] Phase 1 started: added shared patient contract fields in UI (unit/service, specialty, procedure subtype, blocker category/detail, departure time).
- [x] Added billing-threshold logic with global threshold config (`12:00`) and risk levels (`safe`, `info`, `warning`, `critical`).
- [x] Added synchronized shared state store (`StateStore`) powering all panels from one source.
- [x] Added first control-tower card with occupancy-by-service, threshold risk queue, and after-threshold counter.
- [x] Added alert ownership mapping in stakeholder feed (threshold and blocker owners).
- [x] Added role-based mode selector (planner full / nurse light).
- [x] Added 5 simulation presets (late transport, unresolved blocker, late medical validation, occupancy spike, missing critical data).
- [x] Added tutorial/demo script panel for presentations.
- [x] Added dedicated operations page with service/chamber/bed occupancy matrix and bed-click drilldown.
- [x] Added discharge action from matrix to free occupied beds in real time.
- [x] Added free-bed assignment flow from waiting patients directly in matrix view.
- [ ] Next: refine KPI delta visualization for each simulation and mirror this in portfolio narrative.
