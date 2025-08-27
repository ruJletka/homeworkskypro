from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(dict_list: list, state_executed: list, state_canceled: list) -> list:
    assert filter_by_state(dict_list) == state_executed
    assert filter_by_state(dict_list, state="CANCELED") == state_canceled


def test_sort_by_date(dict_list: list, sort_true: list, sort_false: list) -> list:
    assert sort_by_date(dict_list) == sort_true
    assert sort_by_date(dict_list, descending=False) == sort_false
