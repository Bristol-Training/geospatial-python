"""Draw the concept diagrams used in the slides and notes.

The diagrams use made-up points, not the course data, so they only need
numpy, scipy and matplotlib. Run it from the course folder:

    uv run python assets/make_diagrams.py

It saves the PNG files in assets/diagrams/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save files without opening windows

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
from scipy.spatial import Voronoi  # noqa: E402

OUT = Path(__file__).resolve().parent / "diagrams"
RED = "#a6192e"
GREY = "#595959"
PALE = "#e5e6e5"
CATEGORIES = ["#a6192e", "#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#8c564b"]


def save(fig, name):
    """Save a figure as a PNG in assets/diagrams/ and close it."""
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", OUT / name)


def tidy(ax, title):
    """Give a panel a title and hide its axes."""
    ax.set_title(title, color=RED, fontsize=14, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_color(GREY)


def vector_raster():
    """The same place stored as vector shapes, and as a raster grid."""
    fig, (vector, raster) = plt.subplots(1, 2, figsize=(10, 4.6))

    building = Polygon(
        [(1, 5.5), (4, 5.5), (4, 8.5), (1, 8.5)],
        facecolor=PALE,
        edgecolor=GREY,
        linewidth=2,
    )
    vector.add_patch(building)
    vector.plot([0, 10], [3, 4.5], color=GREY, linewidth=4)
    vector.scatter([6, 7.5, 8.5], [7.5, 6, 8], color=RED, s=80, zorder=3)
    vector.text(2.5, 7, "polygon", ha="center", va="center", fontsize=11)
    vector.text(5, 2.6, "line", ha="center", fontsize=11)
    vector.text(7.4, 8.7, "points", ha="center", fontsize=11)
    vector.set_xlim(0, 10)
    vector.set_ylim(0, 10)
    tidy(vector, "Vector: shapes")

    x, y = np.meshgrid(np.linspace(0, 10, 10), np.linspace(0, 10, 10))
    values = np.exp(-((x - 6.5) ** 2 + (y - 6.5) ** 2) / 12)
    raster.imshow(values, origin="lower", extent=(0, 10, 0, 10), cmap="Reds")
    for edge in range(11):
        raster.axhline(edge, color="white", linewidth=0.8)
        raster.axvline(edge, color="white", linewidth=0.8)
    raster.set_xlim(0, 10)
    raster.set_ylim(0, 10)
    tidy(raster, "Raster: a grid of cells")

    save(fig, "vector-raster.png")


def coordinate_systems():
    """A geographic CRS (degrees on a globe) and a projected one (a grid)."""
    fig, (globe, grid) = plt.subplots(1, 2, figsize=(10, 4.6))

    # Orthographic view of the Earth, centred over Europe
    lat0, lon0 = np.radians(40), np.radians(0)

    def project(lat, lon):
        lat, lon = np.radians(lat), np.radians(lon)
        x = np.cos(lat) * np.sin(lon - lon0)
        y = np.cos(lat0) * np.sin(lat) - np.sin(lat0) * np.cos(lat) * np.cos(
            lon - lon0
        )
        visible = (
            np.sin(lat0) * np.sin(lat)
            + np.cos(lat0) * np.cos(lat) * np.cos(lon - lon0)
        ) >= 0
        return np.where(visible, x, np.nan), np.where(visible, y, np.nan)

    globe.add_patch(plt.Circle((0, 0), 1, facecolor=PALE, edgecolor=GREY))
    for lon in range(-180, 180, 30):
        meridian = project(np.linspace(-90, 90, 200), lon)
        globe.plot(*meridian, color=GREY, lw=0.6)
    for lat in range(-60, 90, 30):
        parallel = project(lat, np.linspace(-180, 180, 400))
        globe.plot(*parallel, color=GREY, lw=0.6)
    globe.plot(*project(51.5133, -0.1367), "o", color=RED, markersize=8)
    globe.annotate(
        "51.5133° N, 0.1367° W",
        project(51.5133, -0.1367),
        xytext=(0.35, 1.2),
        fontsize=10,
        arrowprops={"arrowstyle": "-", "color": RED},
        bbox={"facecolor": "white", "edgecolor": "none"},
    )
    globe.set_xlim(-1.1, 1.6)
    globe.set_ylim(-1.1, 1.35)
    tidy(globe, "Geographic: degrees")
    globe.axis("off")

    for value in range(0, 11, 2):
        grid.axhline(value, color=GREY, linewidth=0.6)
        grid.axvline(value, color=GREY, linewidth=0.6)
    grid.plot(6, 5, "o", color=RED, markersize=8)
    grid.annotate(
        "529,397 m east\n181,025 m north",
        (6, 5),
        xytext=(6.4, 6.6),
        fontsize=10,
        arrowprops={"arrowstyle": "-", "color": RED},
        bbox={"facecolor": "white", "edgecolor": "none"},
    )
    grid.set_xlim(0, 10)
    grid.set_ylim(0, 10)
    grid.set_xlabel("metres east", color=GREY)
    grid.set_ylabel("metres north", color=GREY)
    tidy(grid, "Projected: metres")

    save(fig, "coordinate-systems.png")


def spatial_joins():
    """Joining points to the areas they are in, and to their nearest pump."""
    rng = np.random.default_rng(1)
    points = rng.uniform(0.5, 9.5, size=(25, 2))
    fig, (within, nearest) = plt.subplots(1, 2, figsize=(10, 4.6))

    areas = [
        [(0, 0), (5, 0), (5, 10), (0, 10)],
        [(5, 0), (10, 0), (10, 5), (5, 5)],
        [(5, 5), (10, 5), (10, 10), (5, 10)],
    ]
    for colour, corners in zip(CATEGORIES, areas):
        within.add_patch(
            Polygon(corners, facecolor=colour, alpha=0.15, edgecolor=GREY)
        )
    area_of = np.where(points[:, 0] < 5, 0, np.where(points[:, 1] < 5, 1, 2))
    within.scatter(*points.T, c=[CATEGORIES[a] for a in area_of], s=40)
    within.set_xlim(0, 10)
    within.set_ylim(0, 10)
    tidy(within, "sjoin(): which area is each point in?")

    pumps = np.array([[2, 7], [7.5, 8], [6, 2.5]])
    distances = np.linalg.norm(points[:, None] - pumps[None], axis=2)
    closest = distances.argmin(axis=1)
    for point, pump in zip(points, closest):
        nearest.plot(
            *zip(point, pumps[pump]), color=CATEGORIES[pump], lw=0.8, alpha=0.6
        )
    nearest.scatter(*points.T, c=[CATEGORIES[p] for p in closest], s=40)
    nearest.scatter(
        *pumps.T, c=CATEGORIES[:3], marker="^", s=200, edgecolor="black"
    )
    nearest.set_xlim(0, 10)
    nearest.set_ylim(0, 10)
    tidy(nearest, "sjoin_nearest(): which pump is closest?")

    save(fig, "spatial-joins.png")


def voronoi():
    """Voronoi polygons: the area closest to each point."""
    pumps = np.array([[2, 7], [7.5, 8], [6, 2.5], [2.5, 2], [5, 5.5]])
    # Far-away extra points close off the outer polygons
    far = np.array([[-20, -20], [-20, 30], [30, -20], [30, 30]])
    diagram = Voronoi(np.vstack([pumps, far]))

    fig, ax = plt.subplots(figsize=(5, 4.6))
    for number in range(len(pumps)):
        region = diagram.regions[diagram.point_region[number]]
        ax.add_patch(
            Polygon(
                diagram.vertices[region],
                facecolor=CATEGORIES[number],
                alpha=0.2,
                edgecolor=GREY,
                linewidth=1.5,
            )
        )
    ax.scatter(
        *pumps.T, c=CATEGORIES[:5], marker="^", s=200, edgecolor="black"
    )
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    tidy(ax, "Each area is closest to one pump")

    save(fig, "voronoi.png")


def areal_units():
    """The modifiable areal unit problem: same points, different boundaries."""
    rng = np.random.default_rng(3)
    cluster = rng.normal(loc=(5.2, 5.2), scale=0.9, size=(40, 2))
    spread = rng.uniform(0, 10, size=(30, 2))
    points = np.clip(np.vstack([cluster, spread]), 0.1, 9.9)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))

    axes[0].scatter(*points.T, color="black", s=12)
    tidy(axes[0], "The points")

    for ax, size, title in [
        (axes[1], 5, "Counted in 4 areas"),
        (axes[2], 10 / 3, "Counted in 9 areas"),
    ]:
        edges = np.arange(0, 10.01, size)
        counts, _, _ = np.histogram2d(*points.T, bins=[edges, edges])
        ax.imshow(
            counts.T, origin="lower", extent=(0, 10, 0, 10), cmap="Reds"
        )
        for edge in edges:
            ax.axhline(edge, color=GREY, linewidth=1)
            ax.axvline(edge, color=GREY, linewidth=1)
        tidy(ax, title)

    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)

    save(fig, "areal-units.png")


if __name__ == "__main__":
    vector_raster()
    coordinate_systems()
    spatial_joins()
    voronoi()
    areal_units()
