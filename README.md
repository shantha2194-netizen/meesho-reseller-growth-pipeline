# Meesho Reseller Growth & Alert Intelligence Pipeline

An end-to-end offline analytics and alert-intelligence pipeline for monitoring
month-on-month reseller category revenue movements.

The project connects:

Part 1 → SQL Business Query Engine
Part 2 → Python Growth & Validation Engine
Part 3 → Reliable Narrative & Masking Layer
Part 4 → Agent Specification & Mock Agent Runner

The complete workflow works without an API key, paid service, hosted service,
or real message-sending integration.

---

# 1. Project Objective

The project builds a repeatable monitoring workflow that:

1. Generates a fixed-seed reseller/order dataset.
2. Stores the data in SQLite.
3. Answers five business questions using SQL.
4. Calculates month-on-month revenue movement.
5. Applies an 8% threshold using deterministic rules.
6. Validates incoming monthly revenue feeds.
7. Produces stakeholder-ready narrative drafts.
8. Masks raw reseller names in external-facing narratives.
9. Selects the top three flagged categories by absolute MoM movement.
10. Suppresses additional flagged categories for manual review.
11. Separately escalates exact 8% boundary cases.
12. Holds drafted messages for human approval.

---

# 2. Repository Structure

```text
meesho-reseller-growth-pipeline/
│
├── README.md
│
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       └── june_delivered_aov.csv
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       ├── monthly_category_revenue.csv
│       ├── april_category_revenue.csv
│       ├── may_category_revenue.csv
│       └── june_category_revenue.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   ├── narrative.py
│   └── masking.py
│
└── part4_agent/
    ├── agent_spec.md
    └── mock_agent_runner.py

## Official Documentation Referenced

- Python `csv` documentation
- Python `sqlite3` documentation
- Python `pathlib` documentation
- Python `sys` documentation