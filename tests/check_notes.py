"""Run the code in the course notes (notes.qmd) and check the results.

Run it from the course folder:

    uv run python tests/check_notes.py

It downloads the data and the background map tiles, so it needs internet.

To test the notes in Google Colab instead, run

    uv run python tests/check_notes.py --notebook

then upload tests/colab_check.ipynb to Colab and click Runtime → Run all.
"""

import json
import os
import re
import sys
import tempfile
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw plots without opening windows

NOTES = Path(__file__).resolve().parent.parent / "notes.qmd"
CHUNK = re.compile(r"^```\{python\}\n(.*?)^```", re.MULTILINE | re.DOTALL)

# Values stated in the notes, slides and instructor notes
EXPECTED = {
    "addresses": 250,
    "deaths": 489,
    "pumps": 8,
    "broad_street_deaths": 340,
    "deaths_within_100m": 196,
    "most_at_one_address": 15,
    "catchments_with_no_deaths": [3, 6],
}

# The notes measure distance in degrees on purpose, to show this warning
EXPECTED_WARNING = "Geometry is in a geographic CRS"


def run_chunks(chunks, namespace):
    """Run each chunk in turn. Return the number of errors and warnings."""
    errors = warnings_found = 0
    for number, chunk in enumerate(chunks, start=1):
        label = f"chunk {number} ({chunk.strip().splitlines()[0][:50]})"
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                exec(chunk, namespace)
            except Exception as error:
                errors += 1
                print(f"ERROR {label}: {error!r}")
                continue
        messages = {str(warning.message).splitlines()[0] for warning in caught}
        for message in sorted(messages):
            if message.startswith(EXPECTED_WARNING):
                print(f"ok    {label}: expected warning")
            else:
                warnings_found += 1
                print(f"WARN  {label}: {message}")
    return errors, warnings_found


def check_results(ns):
    """Compare the results with the values stated in the materials."""
    deaths, pumps, catchments = ns["deaths"], ns["pumps"], ns["catchments"]
    broad_street = pumps.geometry.iloc[0]
    no_deaths = catchments.loc[catchments["deaths"] == 0, "pump_id"]

    actual = {
        "addresses": len(deaths),
        "deaths": int(deaths["Count"].sum()),
        "pumps": len(pumps),
        "broad_street_deaths": int(ns["deaths_per_pump"].loc[0]),
        "deaths_within_100m": int(ns["deaths_near"]),
        "most_at_one_address": int(deaths["Count"].max()),
        "catchments_with_no_deaths": sorted(no_deaths.tolist()),
    }
    failures = 0
    for name, value in EXPECTED.items():
        passed = actual[name] == value
        failures += not passed
        status = "ok   " if passed else "FAIL "
        print(f"{status} {name}: expected {value}, got {actual[name]}")

    pump_0 = ns["pumps_latlon"].geometry.iloc[0]
    distance = ns["nearest"]["distance"]
    print("\nOther values used in the text:")
    print(f"      pump 0: {pump_0.y:.4f}, {pump_0.x:.4f}")
    print(f"      worst address to pump 0: "
          f"{ns['worst']['geometry'].distance(broad_street):.1f} m")
    print(f"      share nearest Broad Street: {ns['percent'].loc[0]:.1f}%")
    print(f"      distance to nearest pump: mean {distance.mean():.1f} m, "
          f"max {distance.max():.1f} m")
    print(f"      catchment totals match nearest pump: "
          f"{ns['totals'].equals(ns['deaths_per_pump'])}")
    print(f"      geopandas {ns['gpd'].__version__}")
    return failures


def write_notebook(chunks):
    """Write the notes' code, and the checks, as a notebook for Colab."""
    install = (
        '%pip install --quiet "geopandas>=1.0" contextily folium mapclassify'
    )
    checks = "\n".join(
        [
            "import geopandas, pandas, shapely, contextily, folium",
            "for module in [geopandas, pandas, shapely, contextily, folium]:",
            "    print(module.__name__, module.__version__)",
            "",
            "assert len(deaths) == 250",
            'assert deaths["Count"].sum() == 489',
            "assert deaths_per_pump.loc[0] == 340",
            "assert deaths_near == 196",
            'no_deaths = catchments.loc[catchments["deaths"] == 0, "pump_id"]',
            "assert sorted(no_deaths) == [3, 6]",
            'print("All checks passed")',
        ]
    )
    cells = [install, *chunks, checks]
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": cell.strip(),
            }
            for cell in cells
        ],
        "metadata": {
            "kernelspec": {"name": "python3", "display_name": "Python 3"}
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = Path(__file__).resolve().parent / "colab_check.ipynb"
    path.write_text(json.dumps(notebook, indent=1))
    print(f"Wrote {path}")


def main():
    chunks = CHUNK.findall(NOTES.read_text())
    if "--notebook" in sys.argv:
        write_notebook(chunks)
        return
    namespace = {}
    start = Path.cwd()
    with tempfile.TemporaryDirectory() as folder:
        os.chdir(folder)  # keep the downloaded data out of the course folder
        print(f"Running {len(chunks)} chunks from {NOTES.name}\n")
        errors, warnings_found = run_chunks(chunks, namespace)
        print()
        failures = 0 if errors else check_results(namespace)
        os.chdir(start)
    sys.exit(1 if errors or warnings_found or failures else 0)


if __name__ == "__main__":
    main()
