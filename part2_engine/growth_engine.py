import csv


def mom_growth(previous: float, current: float) -> float:
    """Calculate month-on-month revenue growth percentage."""
    if previous == 0:
        return None

    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    """Classify a MoM movement using the 8% threshold."""
    if abs(mom_pct) > threshold:
        return "flagged"

    if abs(mom_pct) < threshold:
        return "not_flagged"

    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    """Validate a monthly category revenue CSV."""

    errors = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for line_number, row in enumerate(reader, start=2):

            month = row["month"]
            category = row["category"]
            revenue = row["revenue"]

            # Missing category
            if not category or not category.strip():
                errors.append(
                    f"line {line_number}: missing category (month={month})"
                )

            # Missing revenue
            if not revenue or not revenue.strip():
                errors.append(
                    f"line {line_number}: missing revenue (category={category})"
                )
                continue

            # Non-numeric revenue
            try:
                revenue_value = float(revenue)
            except ValueError:
                errors.append(
                    f"line {line_number}: revenue not numeric: {revenue!r}"
                )
                continue

            # Negative revenue
            if revenue_value < 0:
                errors.append(
                    f"line {line_number}: negative revenue "
                    f"({revenue_value}) for category={category}"
                )

    return len(errors) == 0, errors