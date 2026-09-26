# Part 3 — Narrative & Prompt Pack

## Purpose

Convert validated month-over-month category revenue changes into a
structured business narrative.

The narrative should be based only on validated data from Part 1 and
Part 2.

---

## Trigger

Generate a narrative when a category's month-over-month revenue change
meets the configured alert threshold.

---

## Input List

The narrative generator receives:

- Previous month
- Current month
- Category
- Previous revenue
- Current revenue
- MoM percentage
- Alert status
- Relevant reseller information where available

---

## Prompt

Create a concise business narrative for the flagged category.

The narrative should include:

1. What changed
2. Magnitude of the change
3. Previous-month revenue
4. Current-month revenue
5. Possible business interpretation based only on available data
6. Recommended follow-up or investigation
7. Chart choice and justification

Do not invent causes that are not supported by the available data.

---

## Checklist

Before producing the narrative:

- Confirm that the feed has passed validation.
- Confirm the previous and current revenue values.
- Confirm the MoM percentage.
- Confirm the alert status.
- Use the correct month and category.
- Avoid unsupported causal claims.
- Mask raw reseller names.
- Confirm that no raw reseller names appear in the final narrative.

---

# Worked Narrative 1 — May Ethnic Wear

## Input

Previous month:

April

Current month:

May

Category:

Ethnic Wear

Previous revenue:

104520.77

Current revenue:

185107.61

MoM growth:

77.1%

Alert status:

flagged

## Narrative

Ethnic Wear revenue increased from 104,520.77 in April to
185,107.61 in May, representing 77.1% month-over-month growth.

This is a significant increase and should be investigated to understand
which reseller-level activity, order volume, or other available business
signals contributed to the change.

The next step is to review the relevant reseller and order-level data
before attributing a specific cause.

## Chart choice

A bar chart can be used to compare April and May revenue directly for
Ethnic Wear because the objective is to show the magnitude of the
month-over-month change.

---

# Worked Narrative 2 — June Ethnic Wear

## Input

Previous month:

May

Current month:

June

Category:

Ethnic Wear

Previous revenue:

185107.61

Current revenue:

76371.53

MoM growth:

-58.74%

Alert status:

flagged

## Narrative

Ethnic Wear revenue decreased from 185,107.61 in May to 76,371.53 in
June, representing a 58.74% month-over-month decline.

This is a substantial decrease and should be investigated using the
available reseller and order-level information.

The analysis should focus on identifying which measurable business
signals changed between May and June before assigning a specific cause.

## Chart choice

A bar chart can be used to compare May and June revenue directly for
Ethnic Wear because the objective is to clearly show the magnitude of
the decline.

---

# Reseller Name Masking

Raw reseller names must not appear in the final narrative.

Use a deterministic alias such as:

- Reseller A
- Reseller B
- Reseller C

The same reseller must receive the same alias whenever it appears again.

---

# Final Safety Check

Before publishing a narrative:

- No raw reseller names should appear.
- No unsupported causes should be presented as facts.
- Revenue values must match the validated feed.
- MoM percentage must match the Python calculation.
- Flag status must match the alert logic.