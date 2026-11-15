# simu-cube-league

Event history, standings and head-to-head stats for
[Simu's Cube](https://cubecobra.com/cube/about/helou?view=primer), built for my playgroup.

<!-- **Live site:** add the link once Pages is live -->

## What it does

* Record match results at an event through a local app
* Build JSON from the CSVs
* View player records, standings and head-to-heads on a static JavaScript + HTML site

## How it works

1. **App** (Streamlit, runs locally) writes results to CSV files in `data/`.
2. **Pipeline** validates the CSVs, loads them into DuckDB, and exports the
   results as JSON.
3. **Site** (static HTML/JS, served by GitHub Pages from `docs/`) reads the JSON.

## Project layout

```
app/        Streamlit entry app
pipeline/   schema.sql, views.sql, load, validate, build
data/       players.csv and events/<date>/matches.csv
docs/       static site (HTML, JS, CSS, generated data/)
tests/      pytest tests and fixtures
Makefile    common commands
```

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Setup

```
uv sync
```

## Usage

| Command         | What it does                                  |
|-----------------|-----------------------------------------------|
| `make run`      | Start the entry app                           |
| `make validate` | Check the CSVs against the schema             |
| `make build`    | Generate the JSON for the site                |
| `make serve`    | Preview the site at http://localhost:8000     |
| `make check`    | Lint, type check, tests and data validation   |
| `make fix`      | Auto-fix lint issues and format code          |

## Adding an event

1. Run `make run` and enter the event date, players and match results.
2. Run `make check`.
3. Commit the new CSVs and push.

## Data format

`data/players.csv` plus one `matches.csv` per event in `data/events/<date>/`.
The columns are defined in [`pipeline/schema.sql`](pipeline/schema.sql) and
[`pipeline/views.sql`](pipeline/views.sql). `make validate` checks your files against them.

<!--
## Deployment

GitHub Actions: a check job, then build and deploy to Pages on push to main.
-->

## Privacy

Player names are shown with their agreement, as first names or handles.

## Using it for your own cube

Fork the repo, replace the CSVs in `data/`, change the site title, and enable GitHub Pages.

## License

MIT