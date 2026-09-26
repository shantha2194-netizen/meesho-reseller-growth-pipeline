# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project implements an end-to-end analytics and alert intelligence pipeline for Meesho reseller growth analysis.

The project is divided into four connected parts:

1. **Part 1 — SQL Analytics**
2. **Part 2 — Python Analytics & Validation**
3. **Part 3 — Business Narrative**
4. **Part 4 — Alert Intelligence Agent**

The complete workflow validates the data, calculates month-over-month (MoM) category revenue movement, identifies significant changes, generates business narratives, suppresses lower-priority alerts, and stops at a human approval checkpoint.

No real messages or emails are sent by the agent.

---

## Project Structure

```text
MEESHO-RESELLER-GROWTH-PIPELINE
│
├── .gitignore
├── README.md
│
├── .vscode
│   └── settings.json
│
├── data
│   ├── generate_dataset.py
│   ├── meesho_reseller.db
│   ├── orders.csv
│   └── resellers.csv
│
├── part1_sql
│   ├── queries.sql
│   └── output
│       └── monthly_category_revenue.csv
│
├── part2_python
│   ├── analytics.py
│   ├── corrupted_feed.csv
│   └── negative_test.csv
│
├── part3_narrative
│   ├── narrative.py
│   └── prompt_pack.md
│
└── part4_agent
    └── agent.py

# Official Documentation Referenced

The following official Python documentation was referenced while implementing the project:

- Python `csv` module:
  https://docs.python.org/3/library/csv.html

- Python `sqlite3` module:
  https://docs.python.org/3/library/sqlite3.html

- Python `pathlib` module:
  https://docs.python.org/3/library/pathlib.html

- Python `sys` module:
  https://docs.python.org/3/library/sys.html