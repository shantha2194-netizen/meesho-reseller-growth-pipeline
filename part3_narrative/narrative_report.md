# Narrative Report

## 1. May — Ethnic Wear

### Context

This section measures the month-on-month revenue movement for the **Ethnic Wear** category from **April to May**.

### Insight

**Fact:** Ethnic Wear revenue increased from **INR 104,520.77 in April** to **INR 185,107.61 in May**, representing **77.10% month-on-month growth**.

The movement is classified as **flagged** because the absolute MoM movement is greater than the 8% monitoring threshold.

### Implication

**Hypothesis:** The regional team should review the April-to-May Ethnic Wear movement at reseller and order level, focusing on changes in order volume, reseller participation, and regional contribution before assigning a specific business cause.

The data establishes the revenue movement, but it does not by itself prove why the increase occurred.

### Refinement Checklist

- **Specificity:** Pass — the category, months, revenue values, and 77.10% MoM movement are explicitly stated.
- **Audience fit:** Pass — the narrative is written for a regional manager and focuses on a business action rather than technical implementation details.
- **Completeness:** Pass — context, factual insight, and implication are all included.
- **Actionability:** Pass — the next step is to examine reseller, order-volume, and regional contribution changes.

---

## 2. June — Ethnic Wear

### Context

This section measures the month-on-month revenue movement for the **Ethnic Wear** category from **May to June**.

### Insight

**Fact:** Ethnic Wear revenue decreased from **INR 185,107.61 in May** to **INR 76,371.53 in June**, representing a **58.74% month-on-month decline**.

The movement is classified as **flagged** because the absolute MoM movement is greater than the 8% monitoring threshold.

### Implication

**Hypothesis:** The regional team should review the May-to-June Ethnic Wear movement at reseller and order level, focusing on changes in order volume, active reseller participation, and regional contribution to determine where the decline originated.

The available revenue data confirms the decline but does not independently establish its business cause.

### Refinement Checklist

- **Specificity:** Pass — the category, months, revenue values, and 58.74% MoM decline are explicitly stated.
- **Audience fit:** Pass — the narrative is written for a regional manager and focuses on a practical business investigation.
- **Completeness:** Pass — context, factual insight, and implication are all included.
- **Actionability:** Pass — the recommended next step is to examine reseller, order-volume, and regional contribution changes.

---

# 3. Chart-Choice Justification

## 3.1 Which month had the highest total revenue?

**Recommended chart: Column chart.**

This is a **univariate comparison across a categorical dimension (month)** with one measure, total revenue. A column chart makes the comparison between April, May, and June easy to understand within a few seconds. The y-axis should start at zero so that the differences in revenue are represented honestly. No legend is required because there is only one revenue series.

The verified monthly totals are:

- April: INR 419,417.43
- May: INR 444,594.25
- June: INR 398,055.24

---

## 3.2 What percentage share does Ethnic Wear represent of April's total revenue?

**Recommended chart: Donut chart.**

This is a **part-to-whole relationship**, where Ethnic Wear revenue is compared with the total April revenue. A donut chart can communicate the share visually, provided the number is also displayed clearly.

Ethnic Wear represents **24.92%** of April's total revenue:

- Ethnic Wear: INR 104,520.77
- April total: INR 419,417.43
- Share: 24.92%

The chart should remain simple and avoid unnecessary 3D effects.

---

## 3.3 How do the four regions compare on total revenue?

**Recommended chart: Horizontal bar chart.**

This is a **univariate comparison across regions**, with region as the categorical dimension and revenue as the measure. A horizontal bar chart allows the four regional values to be compared directly and makes the relative ordering easy to read. The axis should start at zero, and no legend is required because there is only one measure.

The verified regional revenue figures are:

- North: INR 337,125.46
- West: INR 333,106.33
- South: INR 316,736.68
- East: INR 275,098.45

---

# 4. Top-Reseller Narrative and Masking

The Part 1 top-reseller query identified five resellers with total spend
above INR 50,000.

For any externally exposed narrative, the reseller ID is converted into
a coded alias and the raw reseller name is never included.

| Reseller ID | External Alias | Region | Total Spend (INR) |
|---|---|---|---:|
| RS019 | ALIAS-19 | West | 75295.09 |
| RS022 | ALIAS-22 | West | 73882.33 |
| RS012 | ALIAS-12 | South | 69936.46 |
| RS006 | ALIAS-06 | North | 64238.97 |
| RS005 | ALIAS-05 | North | 61825.02 |

### Masked Narrative Example

**Fact:** ALIAS-19 from the West region recorded total spend of
INR 75,295.09 in the Part 1 analysis.

The raw reseller name is intentionally excluded from this narrative.

The same masking policy applies to the remaining four top resellers:

- ALIAS-22 — West
- ALIAS-12 — South
- ALIAS-06 — North
- ALIAS-05 — North

The alias is generated from the reseller ID:

```text
RS019 → ALIAS-19
RS022 → ALIAS-22
RS012 → ALIAS-12
RS006 → ALIAS-06
RS005 → ALIAS-05