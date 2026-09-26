def alias_for(reseller_name):
    """
    Return a deterministic alias for a reseller name.
    """

    aliases = {
        "Mumbai Reseller 1": "Reseller A",
        "Mumbai Reseller 4": "Reseller B",
        "Hyderabad Reseller 6": "Reseller C",
        "Lucknow Reseller 6": "Reseller D",
        "Jaipur Reseller 5": "Reseller E",
        "Ahmedabad Reseller 6": "Reseller F",
    }

    return aliases.get(reseller_name, "Reseller")


def assert_no_raw_names_leak(text, raw_names):
    """
    Check that none of the raw reseller names appear in the text.
    """

    for name in raw_names:
        assert name not in text, f"Raw reseller name leaked: {name}"

    return True


def generate_narrative(
    previous_month,
    current_month,
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    status
):
    """
    Generate a deterministic business narrative
    from validated revenue data.
    """

    direction = "increased" if mom_pct > 0 else "decreased"

    magnitude = abs(mom_pct)

    narrative = (
        f"{category} revenue {direction} from "
        f"{previous_revenue:,.2f} in {previous_month} to "
        f"{current_revenue:,.2f} in {current_month}, "
        f"representing a {magnitude:.2f}% "
        f"month-over-month {'growth' if mom_pct > 0 else 'decline'}.\n\n"
        f"This change is classified as {status}. "
        f"The movement should be investigated using the available "
        f"reseller and order-level information before assigning "
        f"a specific business cause.\n\n"
        f"A bar chart can be used to compare {previous_month} and "
        f"{current_month} revenue directly for {category}, because "
        f"the objective is to show the magnitude of the "
        f"month-over-month change."
    )

    return narrative

if __name__ == "__main__":

    # May Ethnic Wear test
    may_ethnic = generate_narrative(
        previous_month="April",
        current_month="May",
        category="Ethnic Wear",
        previous_revenue=104520.77,
        current_revenue=185107.61,
        mom_pct=77.1,
        status="flagged"
    )

    print(may_ethnic)

    # June Ethnic Wear test
    june_ethnic = generate_narrative(
        previous_month="May",
        current_month="June",
        category="Ethnic Wear",
        previous_revenue=185107.61,
        current_revenue=76371.53,
        mom_pct=-58.74,
        status="flagged"
    )

    print(june_ethnic)

    # Final safety test
    raw_names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
        "Ahmedabad Reseller 6"
    ]

    safe_text = (
        "Reseller A showed strong growth during May. "
        "Further investigation is recommended."
    )

    assert_no_raw_names_leak(safe_text, raw_names)

    print("Final safety test passed: no raw reseller names leaked.")