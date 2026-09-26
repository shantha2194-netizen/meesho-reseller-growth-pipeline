import csv


def mom_growth(previous, current):
    """
    Calculate month-over-month percentage growth.
    """

    if previous == 0:
        return None

    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct, threshold=8.0):
    """
    Determine the alert status based on MoM growth.

    Returns:
        flagged
        not_flagged
        escalate_exact_boundary
    """

    if mom_pct == threshold:
        return "escalate_exact_boundary"

    if mom_pct > threshold:
        return "flagged"

    return "not_flagged"


def validate_feed(csv_path):
    """
    Validate the monthly category revenue CSV.

    Checks:
    - Missing category
    - Missing revenue
    - Non-numeric revenue
    - Negative revenue
    """

    errors = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row_number, row in enumerate(reader, start=2):

            # Missing category
            if not row["category"] or not row["category"].strip():
                errors.append(
                    f"Row {row_number}: missing category"
                )

            # Missing revenue
            if not row["revenue"] or not row["revenue"].strip():
                errors.append(
                    f"Row {row_number}: missing revenue"
                )
                continue

            # Non-numeric revenue
            try:
                revenue = float(row["revenue"])
            except ValueError:
                errors.append(
                    f"Row {row_number}: non-numeric revenue"
                )
                continue

            # Negative revenue
            if revenue < 0:
                errors.append(
                    f"Row {row_number}: negative revenue"
                )

    return errors