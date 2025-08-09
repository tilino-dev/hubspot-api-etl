from src.transform import _flatten

def test_flatten_empty():
    assert _flatten([]).empty

def test_flatten_basic():
    records = [
        {"id": "123", "properties": {"email": "a@example.com", "createdate": "2024-01-01T00:00:00Z"}},
        {"id": "124", "properties": {"email": "b@example.com", "createdate": "2024-01-02T00:00:00Z"}},
    ]
    df = _flatten(records)
    assert "email" in df.columns
    assert df.loc[0, "hs_object_id"] == 123
