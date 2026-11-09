# Geospatial Python

This course introduces working with maps and location data in Python, using one of the most famous stories in public health. In 1854, John Snow mapped cholera deaths in London to find the source of an outbreak. You will recreate his analysis, using the geopandas library to load, map and analyse his data.

The course takes three hours and runs in Google Colab.

**Course website:** <https://bristol-training.github.io/geospatial-python/>

## Prerequisites

- Basic Python: variables, lists, functions and importing packages.
- Some experience with pandas is helpful but not required.
- No experience of maps or geospatial data is needed.
- A Google account, to use Colab.

## What you will learn

- How to load and explore location data with geopandas.
- What coordinate reference systems are and why they matter.
- How to make static and interactive maps.
- How to combine datasets by location, for example finding the nearest water pump to each address.
- How to think critically about what maps can and cannot tell us.

## What's in this folder

```
├── _quarto.yml          site settings: title, header bar, page and slide formats
├── _brand.yml           colours, logo and fonts
├── custom.scss          custom styles for the site and slides
├── index.qmd            home page: the course notes, with the slides embedded at the top
├── slides.qmd           the presentation
├── instructor.qmd       instructor notes: timings, checkpoints, the numbers to expect
├── notebooks/           the Colab notebook attendees type into
├── pyproject.toml       Python packages needed to render the site
├── tests/               a script that runs the notes' code and checks the numbers
├── assets/              logo and images
└── docs/                the rendered website (created by quarto render, commit it)
```

## Data

The course uses Robin Wilson's digitised version of John Snow's map, from <https://johnsnow.rtwilson.com/>. The notes and the notebook download it from his site, so it is not stored in this repository.

## Building the course locally

You need [uv](https://docs.astral.sh/uv/). It installs Python, Quarto and the packages in `pyproject.toml`:

```bash
git clone https://github.com/Bristol-Training/geospatial-python.git
cd geospatial-python
uv sync
uv run python tests/check_notes.py
uv run quarto preview
```

`tests/check_notes.py` runs the code in the notes and checks the numbers quoted in the materials. To run the same checks in Google Colab, run `uv run python tests/check_notes.py --notebook`, upload `tests/colab_check.ipynb` to Colab and click **Runtime → Run all**. `quarto preview` opens the course in your browser and reloads it whenever you save a `.qmd` file. Both download the data, so you need an internet connection.

## Publishing

GitHub only publishes what is in `docs/`, so after changing the materials:

```bash
uv run quarto render
git add -A
git commit -m "Update materials"
git push
```

The first time, set up GitHub Pages in **Settings → Pages**: set **Source** to **Deploy from a branch**, **Branch** to `main` and the folder to `/docs`.

## Contributing

Corrections and suggestions are welcome.

**Spotted a problem?** [Open an issue](https://github.com/Bristol-Training/geospatial-python/issues) saying which page and section it's in.

**Small fix, like a typo?** Open the `.qmd` file on GitHub, click the pencil icon (**Edit this file**), make the change and click **Propose changes**. GitHub makes a copy of the repository for you and opens a pull request.

**Bigger change?**

1. Fork the repository on GitHub and clone your fork.
2. Create a branch: `git checkout -b my-change`.
3. Edit the `.qmd` files and check the result with `quarto preview`.
4. Commit and push your branch, then open a pull request on GitHub describing what you changed and why.

Only commit the `.qmd` files (and any new images in `assets/`), not the `docs/` folder. The maintainer re-renders the website after merging.

## Credits

Developed by the [Jean Golding Institute](https://www.bristol.ac.uk/golding/).

Data digitised from John Snow's map by [Robin Wilson](https://johnsnow.rtwilson.com/).

Jean Golding Institute © CC-BY 4.0
