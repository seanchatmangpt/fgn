def impute(values, replacement=0):
    return [replacement if value is None else value for value in values]


def label(values):
    return [(value, f"item-{index}") for index, value in enumerate(values)]


def test_data_imputation():
    assert impute([1, None, 3]) == [1, 0, 3]


def test_data_labelling():
    assert label(["a", "b"]) == [("a", "item-0"), ("b", "item-1")]


def test_data_sorting():
    assert sorted([3, 1, 2]) == [1, 2, 3]
