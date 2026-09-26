import sys
import csv
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT / "part2_python"))
sys.path.append(str(PROJECT_ROOT / "part3_narrative"))


# ============================================================
# IMPORT FUNCTIONS FROM PART 2
# ============================================================

from analytics import (
    mom_growth,
    is_flagged,
    validate_feed
)


# ============================================================
# IMPORT FUNCTIONS FROM PART 3
# ============================================================

from narrative import (
    generate_narrative,
    assert_no_raw_names_leak
)


# ============================================================
# PART 4 - FEED VALIDATION
# ============================================================

def validate_input_feed(csv_path):
    """
    Validate the input feed before any analytics are performed.

    If validation errors exist, the agent must stop.
    """

    errors = validate_feed(csv_path)

    if errors:
        return {
            "feed_status": "invalid",
            "errors": errors,
            "status": "hard_stop"
        }

    return {
        "feed_status": "valid",
        "errors": [],
        "status": "ready"
    }


# ============================================================
# PART 4 - CALCULATE MOM
# ============================================================

def calculate_mom_from_csv(csv_path):
    """
    Read monthly category revenue data and calculate
    month-over-month growth for each category.
    """

    data = {}

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            month = row["month"]
            category = row["category"]
            revenue = float(row["revenue"])

            if category not in data:
                data[category] = {}

            data[category][month] = revenue

    results = []

    for category, monthly_data in data.items():

        # April -> May
        if "April" in monthly_data and "May" in monthly_data:

            previous = monthly_data["April"]
            current = monthly_data["May"]

            mom_pct = mom_growth(previous, current)

            results.append({
                "previous_month": "April",
                "current_month": "May",
                "category": category,
                "previous_revenue": previous,
                "current_revenue": current,
                "mom_pct": mom_pct
            })

        # May -> June
        if "May" in monthly_data and "June" in monthly_data:

            previous = monthly_data["May"]
            current = monthly_data["June"]

            mom_pct = mom_growth(previous, current)

            results.append({
                "previous_month": "May",
                "current_month": "June",
                "category": category,
                "previous_revenue": previous,
                "current_revenue": current,
                "mom_pct": mom_pct
            })

    return results


# ============================================================
# PART 4 - CLASSIFY MOM RESULTS
# ============================================================

def classify_mom_results(mom_results, threshold=8.0):
    """
    Classify each MoM result using the Part 2 threshold logic.

    Part 4 treats movements above the threshold in either
    direction as flagged.
    """

    classified_results = []

    for result in mom_results:

        status = is_flagged(
            abs(result["mom_pct"]),
            threshold
        )

        result_with_status = result.copy()
        result_with_status["status"] = status

        classified_results.append(result_with_status)

    return classified_results


# ============================================================
# PART 4 - SELECT TOP FLAGGED MOVEMENTS
# ============================================================

def select_top_flagged(classified_results, top_n=3):
    """
    Select the top flagged movements based on absolute
    month-over-month percentage.
    """

    flagged = [
        result
        for result in classified_results
        if result["status"] == "flagged"
    ]

    flagged.sort(
        key=lambda result: abs(result["mom_pct"]),
        reverse=True
    )

    return flagged[:top_n]


# ============================================================
# PART 4 - SUPPRESS REMAINING FLAGGED MOVEMENTS
# ============================================================

def get_suppressed_flagged(classified_results, top_n=3):
    """
    Return flagged movements that fall outside the Top N.
    """

    flagged = [
        result
        for result in classified_results
        if result["status"] == "flagged"
    ]

    flagged.sort(
        key=lambda result: abs(result["mom_pct"]),
        reverse=True
    )

    return flagged[top_n:]


# ============================================================
# PART 4 - GENERATE NARRATIVE DRAFTS
# ============================================================

def generate_drafts(top_results):
    """
    Generate business narratives for the selected Top-N
    flagged movements using the Part 3 narrative function.
    """

    drafts = []

    for result in top_results:

        narrative = generate_narrative(
            previous_month=result["previous_month"],
            current_month=result["current_month"],
            category=result["category"],
            previous_revenue=result["previous_revenue"],
            current_revenue=result["current_revenue"],
            mom_pct=result["mom_pct"],
            status=result["status"]
        )

        drafts.append({
            "previous_month": result["previous_month"],
            "current_month": result["current_month"],
            "category": result["category"],
            "mom_pct": result["mom_pct"],
            "narrative": narrative
        })

    return drafts


# ============================================================
# PART 4 - NARRATIVE SAFETY
# ============================================================

def validate_narrative_safety(drafts, raw_names):
    """
    Verify that no raw reseller names appear
    in generated narratives.
    """

    for draft in drafts:

        assert_no_raw_names_leak(
            draft["narrative"],
            raw_names
        )

    return True


# ============================================================
# PART 4 - STRUCTURED OUTPUT
# ============================================================

def build_agent_output(
    may_drafts,
    june_drafts,
    suppressed_may,
    suppressed_june,
    boundary_results
):
    """
    Build the final structured output for the agent.

    The agent prepares the information for human review.
    It does not send any real communication.
    """

    output = {
        "feed_status": "valid",

        "may": {
            "alerts": may_drafts,
            "suppressed": suppressed_may
        },

        "june": {
            "alerts": june_drafts,
            "suppressed": suppressed_june
        },

        "escalations": boundary_results,

        "approval": {
            "required": True,
            "approved": False
        }
    }

    return output


# ============================================================
# PART 4 - FULL AGENT RUNNER
# ============================================================

def run_agent(csv_path):
    """
    Run the complete agent workflow.

    1. Validate feed
    2. Stop if invalid
    3. Calculate MoM
    4. Classify movements
    5. Separate exact-boundary escalations
    6. Select Top 3
    7. Suppress remaining flagged movements
    8. Generate narratives
    9. Perform safety check
    10. Prepare structured output
    11. Stop at human approval checkpoint
    """

    validation = validate_input_feed(csv_path)

    if validation["status"] == "hard_stop":

        return {
            "feed_status": "invalid",
            "errors": validation["errors"],
            "status": "hard_stop",
            "mom_calculated": False,
            "narratives_generated": False,
            "approval": {
                "required": False,
                "approved": False
            }
        }

    # --------------------------------------------------------
    # Calculate MoM
    # --------------------------------------------------------

    mom_results = calculate_mom_from_csv(csv_path)

    # --------------------------------------------------------
    # Classify results
    # --------------------------------------------------------

    classified_results = classify_mom_results(mom_results)

    # --------------------------------------------------------
    # Separate exact-boundary escalations
    # --------------------------------------------------------

    boundary_results = [
        result
        for result in classified_results
        if result["status"] == "escalate_exact_boundary"
    ]

    # --------------------------------------------------------
    # May results
    # --------------------------------------------------------

    may_results = [
        result
        for result in classified_results
        if result["previous_month"] == "April"
        and result["current_month"] == "May"
    ]

    # --------------------------------------------------------
    # June results
    # --------------------------------------------------------

    june_results = [
        result
        for result in classified_results
        if result["previous_month"] == "May"
        and result["current_month"] == "June"
    ]

    # --------------------------------------------------------
    # Select Top 3
    # --------------------------------------------------------

    top_may = select_top_flagged(may_results)
    top_june = select_top_flagged(june_results)

    # --------------------------------------------------------
    # Suppress remaining flagged movements
    # --------------------------------------------------------

    suppressed_may = get_suppressed_flagged(may_results)
    suppressed_june = get_suppressed_flagged(june_results)

    # --------------------------------------------------------
    # Generate narratives
    # --------------------------------------------------------

    may_drafts = generate_drafts(top_may)
    june_drafts = generate_drafts(top_june)

    # --------------------------------------------------------
    # Narrative safety check
    # --------------------------------------------------------

    raw_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
        "Ahmedabad Reseller 6"
    ]

    all_drafts = may_drafts + june_drafts

    validate_narrative_safety(
        all_drafts,
        raw_names
    )

    # --------------------------------------------------------
    # Build structured output
    # --------------------------------------------------------

    return build_agent_output(
        may_drafts=may_drafts,
        june_drafts=june_drafts,
        suppressed_may=suppressed_may,
        suppressed_june=suppressed_june,
        boundary_results=boundary_results
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("Part 2 functions imported successfully.")
    print("Part 3 functions imported successfully.")
    print("Part 4 agent setup is ready.")

    # --------------------------------------------------------
    # Clean feed
    # --------------------------------------------------------

    clean_feed = (
        PROJECT_ROOT
        / "part1_sql"
        / "output"
        / "monthly_category_revenue.csv"
    )

    print("\nRunning clean feed...")

    clean_result = run_agent(clean_feed)

    print("Feed status:", clean_result["feed_status"])
    print("Human approval required:",
          clean_result["approval"]["required"])
    print("Approved:",
          clean_result["approval"]["approved"])

    # --------------------------------------------------------
    # Corrupted feed hard-stop test
    # --------------------------------------------------------

    corrupted_feed = (
        PROJECT_ROOT
        / "part2_python"
        / "corrupted_feed.csv"
    )

    print("\nRunning corrupted feed test...")

    corrupted_result = run_agent(corrupted_feed)

    print("Feed status:",
          corrupted_result["feed_status"])

    print("Status:",
          corrupted_result["status"])

    print("MoM calculated:",
          corrupted_result["mom_calculated"])

    print("Narratives generated:",
          corrupted_result["narratives_generated"])

    print("Errors:")

    for error in corrupted_result["errors"]:
        print("-", error)

    # --------------------------------------------------------
    # Exact 8% boundary test
    # --------------------------------------------------------

    print("\nRunning exact 8% boundary test...")

    boundary_previous = 100000.00
    boundary_current = 108000.00

    boundary_mom = mom_growth(
        boundary_previous,
        boundary_current
    )

    boundary_status = is_flagged(
        boundary_mom,
        threshold=8.0
    )

    print("Previous revenue:", boundary_previous)
    print("Current revenue:", boundary_current)
    print("MoM:", boundary_mom, "%")
    print("Status:", boundary_status)

    print("\nAll Part 4 tests completed.")