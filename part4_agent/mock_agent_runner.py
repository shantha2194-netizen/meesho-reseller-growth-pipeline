import csv
import json
import sys
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PART2_DIR = BASE_DIR / "part2_engine"
PART3_DIR = BASE_DIR / "part3_narrative"

sys.path.insert(0, str(PART2_DIR))
sys.path.insert(0, str(PART3_DIR))


# ---------------------------------------------------------
# Import Part 2 functions UNMODIFIED
# ---------------------------------------------------------

from growth_engine import (
    validate_feed,
    mom_growth,
    is_flagged,
)


# ---------------------------------------------------------
# Import Part 3 narrative function
# ---------------------------------------------------------

from narrative import generate_narrative


# ---------------------------------------------------------
# Helper: read monthly revenue CSV
# ---------------------------------------------------------

def read_monthly_revenue(csv_path):
    """Read monthly category revenue from CSV."""

    rows = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(
                {
                    "month": row["month"],
                    "category": row["category"],
                    "revenue": float(row["revenue"]),
                    "n_orders": int(row["n_orders"]),
                }
            )

    return rows


# ---------------------------------------------------------
# Helper: calculate MoM for every category
# ---------------------------------------------------------

def calculate_mom(previous_csv, current_csv):
    """Calculate MoM movement for matching categories."""

    previous_rows = read_monthly_revenue(previous_csv)
    current_rows = read_monthly_revenue(current_csv)

    previous = {
        row["category"]: row["revenue"]
        for row in previous_rows
    }

    results = []

    for row in current_rows:
        category = row["category"]

        if category not in previous:
            continue

        previous_revenue = previous[category]
        current_revenue = row["revenue"]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        status = is_flagged(mom_pct)

        results.append(
            {
                "category": category,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
                "mom_pct": mom_pct,
                "status": status,
            }
        )

    return results


# ---------------------------------------------------------
# Helper: create narrative
# ---------------------------------------------------------

def create_draft(month, previous_month, result):
    """Create a deterministic Part 3 narrative draft."""

    return generate_narrative(
        previous_month=previous_month,
        current_month=month,
        category=result["category"],
        previous_revenue=result["previous_revenue"],
        current_revenue=result["current_revenue"],
        mom_pct=result["mom_pct"],
        status=result["status"],
    )


# ---------------------------------------------------------
# Main agent runner
# ---------------------------------------------------------

def run(
    month,
    previous_month_csv,
    current_month_csv,
    previous_month_name,
):
    """
    Execute the complete mock agent workflow.

    Returns one structured JSON-compatible dictionary.
    """

    # -----------------------------------------------------
    # 1. Validate current-month feed FIRST
    # -----------------------------------------------------

    valid, validation_errors = validate_feed(
        current_month_csv
    )

    # -----------------------------------------------------
    # 2. Hard Stop if validation fails
    # -----------------------------------------------------

    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # -----------------------------------------------------
    # 3. Calculate MoM for every category
    # -----------------------------------------------------

    results = calculate_mom(
        previous_month_csv,
        current_month_csv,
    )

    # -----------------------------------------------------
    # 4. Classify categories
    # -----------------------------------------------------

    flagged = []
    escalated = []

    for result in results:

        if result["status"] == "flagged":
            flagged.append(result)

        elif result["status"] == "escalate_exact_boundary":
            escalated.append(result["category"])

    # -----------------------------------------------------
    # 5. Sort flagged categories by absolute MoM
    # -----------------------------------------------------

    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True,
    )

    # -----------------------------------------------------
    # 6. Draft only the top 3
    # -----------------------------------------------------

    top_three = flagged[:3]

    # -----------------------------------------------------
    # 7. Suppress remaining flagged categories
    # -----------------------------------------------------

    suppressed = [
        item["category"]
        for item in flagged[3:]
    ]

    # -----------------------------------------------------
    # 8. Generate structured flagged output
    # -----------------------------------------------------

    flagged_output = []

    for result in top_three:

        narrative = create_draft(
            month=month,
            previous_month=previous_month_name,
            result=result,
        )

        flagged_output.append(
            {
                "category": result["category"],
                "mom_pct": result["mom_pct"],
                "previous_revenue": result["previous_revenue"],
                "current_revenue": result["current_revenue"],
                "drafted": True,
                "message": narrative,
            }
        )

    # -----------------------------------------------------
    # 9. Return final structured result
    # -----------------------------------------------------

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }


# ---------------------------------------------------------
# Command-line test scenarios
# ---------------------------------------------------------

if __name__ == "__main__":

    fixtures = BASE_DIR / "part2_engine" / "fixtures"

    # May scenario: April → May
    may_result = run(
        month="May",
        previous_month_csv=fixtures / "april_category_revenue.csv",
        current_month_csv=fixtures / "may_category_revenue.csv",
        previous_month_name="April",
    )

    print("\n===== MAY SCENARIO =====")
    print(json.dumps(may_result, indent=2))

    # June scenario: May → June
    june_result = run(
        month="June",
        previous_month_csv=fixtures / "may_category_revenue.csv",
        current_month_csv=fixtures / "june_category_revenue.csv",
        previous_month_name="May",
    )

    print("\n===== JUNE SCENARIO =====")
    print(json.dumps(june_result, indent=2))

    # Corrupted-feed scenario
    corrupted_result = run(
        month="July",
        previous_month_csv=fixtures / "june_category_revenue.csv",
        current_month_csv=fixtures / "corrupted_feed.csv",
        previous_month_name="June",
    )

    print("\n===== CORRUPTED FEED SCENARIO =====")
    print(json.dumps(corrupted_result, indent=2))