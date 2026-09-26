from pathlib import Path

from growth_engine import mom_growth, is_flagged, validate_feed


BASE_DIR = Path(__file__).parent
FIXTURES_DIR = BASE_DIR / "fixtures"


def test_may_ethnic_wear_growth():
    # GIVEN April → May Ethnic Wear revenue
    previous = 104520.77
    current = 185107.61

    # WHEN MoM growth is calculated
    mom_pct = mom_growth(previous, current)

    # THEN the result should be 77.1% and flagged
    assert mom_pct == 77.1
    assert is_flagged(mom_pct) == "flagged"


def test_june_beauty_growth():
    # GIVEN May → June Beauty & Personal Care revenue
    previous = 35542.11
    current = 37559.07

    # WHEN MoM growth is calculated
    mom_pct = mom_growth(previous, current)

    # THEN the result should be 5.67% and not flagged
    assert mom_pct == 5.67
    assert is_flagged(mom_pct) == "not_flagged"


def test_exact_8_percent_boundary():
    # GIVEN a synthetic movement exactly at the threshold
    previous = 100000
    current = 108000

    # WHEN MoM growth is calculated
    mom_pct = mom_growth(previous, current)

    # THEN it must require human escalation
    assert mom_pct == 8.0
    assert is_flagged(mom_pct) == "escalate_exact_boundary"


def test_corrupted_feed():
    # GIVEN the official corrupted fixture
    corrupted_file = FIXTURES_DIR / "corrupted_feed.csv"

    # WHEN the feed is validated
    valid, errors = validate_feed(str(corrupted_file))

    # THEN validation must fail with exactly 3 required errors
    expected_errors = [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert valid is False
    assert errors == expected_errors


def test_clean_monthly_revenue_feed():
    # GIVEN the validated Part 1 output copied into the fixtures folder
    clean_file = FIXTURES_DIR / "monthly_category_revenue.csv"

    # WHEN the feed is validated
    valid, errors = validate_feed(str(clean_file))

    # THEN it should contain no validation errors
    assert valid is True
    assert errors == []


if __name__ == "__main__":
    test_may_ethnic_wear_growth()
    test_june_beauty_growth()
    test_exact_8_percent_boundary()
    test_corrupted_feed()
    test_clean_monthly_revenue_feed()

    print("All Part 2 tests passed.")