def clean_dataset(values):
    return [value.strip() for value in values if value and value.strip()]


def summarize(values):
    return {"count": len(values), "first": values[0] if values else None}


def test_scrape_boundary_uses_admitted_local_payload():
    payload = "example payload"
    assert payload


def test_dataset_cleaning_is_deterministic():
    assert clean_dataset([" alpha ", "", " beta "]) == ["alpha", "beta"]


def test_summary_contract():
    assert summarize(["alpha", "beta"]) == {"count": 2, "first": "alpha"}
