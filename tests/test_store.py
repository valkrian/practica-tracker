from practica_tracker.store import Entry, append_entry, read_entries, export_xlsx
from pathlib import Path


def test_append_and_read(tmp_path):
    db = tmp_path / "practica.csv"
    e = Entry.new(description="Test 1", date_iso="2026-01-02", time_str="10:00", tags="py", duration_minutes=30)
    append_entry(db, e)
    loaded = read_entries(db)
    assert len(loaded) == 1
    assert loaded[0].description == "Test 1"


def test_export_xlsx(tmp_path):
    db = tmp_path / "practica.csv"
    e = Entry.new(description="Test 2", date_iso="2026-01-02", time_str="11:00", tags="py", duration_minutes=15)
    append_entry(db, e)
    xlsx = tmp_path / "out.xlsx"
    # openpyxl may not be installed in environment; if so, skip test
    try:
        export_xlsx(db, xlsx)
    except RuntimeError:
        import pytest
        pytest.skip("openpyxl not installed")
    assert xlsx.exists()
