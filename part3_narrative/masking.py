def alias_for(reseller_id: str) -> str:
    """Convert a reseller ID into an external-facing alias."""
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(
    text: str,
    reseller_names: list[str]
) -> bool:
    """Return False if any raw reseller name appears in the text."""

    for reseller_name in reseller_names:
        if reseller_name in text:
            return False

    return True


if __name__ == "__main__":
    # Positive test
    safe_text = (
        "ALIAS-19 from the West region showed the highest "
        "reseller-level revenue."
    )

    names = [
        "Mumbai Reseller 1",
        "Mumbai Reseller 4",
        "Hyderabad Reseller 6",
        "Lucknow Reseller 6",
        "Jaipur Reseller 5",
    ]

    assert alias_for("RS019") == "ALIAS-19"
    assert assert_no_raw_names_leak(safe_text, names) is True

    # Negative test
    unsafe_text = (
        "Mumbai Reseller 1 showed strong revenue performance."
    )

    assert assert_no_raw_names_leak(unsafe_text, names) is False

    print("Masking tests passed.")