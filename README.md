# Automated Customer Ticket Triage & SLA Engine

A lightweight, automated Python backend pipeline designed to parse unstructured customer support ticket payloads, evaluate urgency through rule-based regex heuristics, calculate real-time SLA deadlines, and flag breaches.

## Key Features
- **Heuristic Ticket Classification**: Inspects subject patterns using regular expressions to categorize priority (`URGENT`, `MEDIUM`, `LOW`).
- **Dynamic SLA Evaluation**: Calculates elapsed ticket windows against business-defined SLAs via Python `datetime` module.
- **Automated Reporting**: Exports processed ticket health metrics and resolution urgency to CSV for downstream support operations.
- **Robust Parsing & Handling**: Gracefully handles missing files, malformed JSON structures, and incomplete ticket objects.

## Tech Stack
- **Language**: Python 3.x
- **Core Modules**: `json`, `csv`, `re` (Regex), `datetime`

## Project Structure
```text
ticket-triage-sla-engine/
├── tickets.json          # Raw customer ticket payloads
├── triage_engine.py      # Core classification, SLA computation, and export logic
├── triage_summary.csv    # Generated metrics output report
└── README.md             # Project documentation
