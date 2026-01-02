"""Flask web UI for practica-tracker.

Endpoints (UML-like):

    [GET /] -> list entries
    [GET/POST /add] -> create entry -> store.append_entry()
    [GET /export/csv] -> send practica.csv
    [GET /export/xlsx] -> export_xlsx() -> send .xlsx

This module depends on the store layer and renders templates in `templates/`.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from pathlib import Path
from practica_tracker.store import Entry, append_entry, read_entries, export_xlsx
import tempfile

app = Flask(__name__)
app.secret_key = "dev-key-for-local"

DB = Path("practica.csv")


@app.route("/")
def index():
    entries = read_entries(DB)
    # show most recent first
    entries = sorted(entries, key=lambda e: (e.date, e.time), reverse=True)
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        if not description:
            flash("Description is required", "danger")
            return redirect(url_for("add"))
        date_iso = request.form.get("date") or None
        time_str = request.form.get("time") or None
        tags = request.form.get("tags", "")
        duration = request.form.get("duration", 0) or 0
        entry = Entry.new(description=description, date_iso=date_iso, time_str=time_str, tags=tags, duration_minutes=duration)
        append_entry(DB, entry)
        flash("Entry added", "success")
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/export/xlsx")
def export_xlsx_route():
    tmp = tempfile.NamedTemporaryFile(prefix="practica-", suffix=".xlsx", delete=False)
    tmp.close()
    export_xlsx(DB, Path(tmp.name))
    return send_file(tmp.name, as_attachment=True, download_name="practica.xlsx")


@app.route("/export/csv")
def export_csv_route():
    if not DB.exists():
        flash("No data to export", "warning")
        return redirect(url_for("index"))
    return send_file(DB, as_attachment=True, download_name=DB.name)


if __name__ == "__main__":
    app.run(debug=True)
