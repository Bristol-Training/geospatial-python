# Geospatial Python

## About this course

Most health data has a location attached: where a patient lives, where a GP surgery is, where a case of a disease was reported. This course introduces working with maps and location data in Python, using one of the most famous stories in public health: John Snow's map of the 1854 cholera outbreak in Soho, London.

Attendees recreate Snow's analysis with the geopandas library, and learn the ideas behind it: vector and raster data, coordinate reference systems, spatial joins and catchment areas. The course finishes by asking what a map can and cannot tell us.

The course takes three hours and runs in Google Colab, so attendees need a Google account and basic Python, but no experience of geospatial data. The notes are written so they can also be used for self-study.

**Course website:** <https://bristol-training.github.io/geospatial-python/>

## What is in this repository

| File or folder | What it is |
|---|---|
| `index.qmd` | The course home page, with the learning objectives, outline and links |
| `slides.qmd` | The slides: the story, then for each section some theory and one activity (together, your turn, answer), with the steps in the speaker notes (press S) |
| `notes.qmd` | The notes. Reference for attendees, and written so they can be used for self-study, with a "Try it yourself" activity and answer for each section |
| `instructor.qmd` | A quick-glance guide for the instructor: timings, key messages, things not to forget, checkpoints and the numbers to expect |
| `notebooks/` | The Colab notebook attendees type into |
| `tests/check_notes.py` | Runs the code in the notes and checks the numbers quoted in the materials |
| `assets/` | Logo and pictures. `assets/make_diagrams.py` draws the diagrams in `assets/diagrams/` |
| `_quarto.yml`, `custom.scss`, `_brand.yml` | Site settings, styles and branding |
| `pyproject.toml`, `uv.lock` | The Python packages needed to render the course |
| `.github/` | The GitHub Action that renders the website and publishes it to the `gh-pages` branch on every push to `main` |

## Teaching the course

Read `instructor.qmd` first. Before teaching, run the checks below, and keep a backup copy of the data in case its website is down on the day.

## Building the course locally

You need [uv](https://docs.astral.sh/uv/). It installs Python, Quarto and the packages in `pyproject.toml`:

```bash
git clone https://github.com/Bristol-Training/geospatial-python.git
cd geospatial-python
uv sync
uv run python tests/check_notes.py
uv run quarto preview
```

- `tests/check_notes.py` runs the code in the notes and checks the numbers quoted in the materials. To run the same checks in Google Colab, run `uv run python tests/check_notes.py --notebook`, upload `tests/colab_check.ipynb` to Colab and click **Runtime → Run all**.
- `quarto preview` opens the course in your browser and reloads it whenever you save a `.qmd` file. The rendered site goes in `docs/`, which isn't committed.
- To redraw the diagrams, run `uv run python assets/make_diagrams.py`.

Both the checks and the preview download the data, so you need an internet connection.

## Data

The course uses Robin Wilson's digitised version of John Snow's map, from <https://johnsnow.rtwilson.com/>. His website lists teaching as one of its uses. The notes and the notebook download it from his site, so it is not stored in this repository.

## Publishing

The website is published automatically. Every push to `main` runs the GitHub Action in `.github/workflows/publish.yml`, which installs the packages in `uv.lock`, renders the site and pushes it to the `gh-pages` branch. GitHub Pages serves the site from that branch. You can also run the Action by hand from the **Actions** tab.

Code chunks are *frozen* (`freeze: auto` in `_quarto.yml`): their results are saved, and a page's code only runs again when that page changes. The Action keeps the saved results in its cache, so you don't need to render locally before pushing.

To add a Python package, run `uv add <package>` and commit the changed `pyproject.toml` and `uv.lock`.

## Contributing

Corrections and suggestions are welcome.

**Spotted a problem?** [Open an issue](https://github.com/Bristol-Training/geospatial-python/issues) saying which page and section it's in.

**Small fix, like a typo?** Open the `.qmd` file on GitHub, click the pencil icon (**Edit this file**), make the change and click **Propose changes**. GitHub makes a copy of the repository for you and opens a pull request.

**Bigger change?**

1. Fork the repository on GitHub and clone your fork.
2. Create a branch: `git checkout -b my-change`.
3. Edit the `.qmd` files and check the result with `quarto preview`.
4. Commit and push your branch, then open a pull request on GitHub describing what you changed and why.

Commit only the source files: the `.qmd` files and any new images in `assets/`. Don't commit `docs/`: it's ignored by git, and the website is rebuilt automatically after merging.

## Credits

Developed by the [Jean Golding Institute](https://www.bristol.ac.uk/golding/). Data digitised from John Snow's map by [Robin Wilson](https://johnsnow.rtwilson.com/).

Jean Golding Institute © CC-BY 4.0
