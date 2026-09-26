# Part 4 — Agent Specification

## 1. Goal

Keep Meesho category managers informed of categories whose month-on-month
revenue movement exceeds the 8% threshold, while requiring human approval
before any drafted message is considered sent.

---

## 2. Tools

The monitoring agent uses the following functions:

### Part 2 — Growth Engine

- `validate_feed()`
- `mom_growth()`
- `is_flagged()`

These functions provide input validation, month-on-month calculation,
and threshold classification.

### Part 3 — Narrative Layer

The agent uses the Part 3 deterministic narrative template to create a
stakeholder-ready draft from verified numbers.

No external API, API key, email service, or network call is required.

---

## 3. Memory / State

Between monthly runs, the workflow needs the previous month's revenue
for each category.

This previous-month value is required to calculate:

```text
Month-on-Month Growth =
((Current Revenue - Previous Revenue) / Previous Revenue) × 100