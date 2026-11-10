# HelioField imagery archive

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23935774.svg)](https://doi.org/10.5281/zenodo.23935774)
[![Status](https://sr-dash.github.io/status/badges/heliofield-imagery.svg)](https://sr-dash.github.io/status/#heliofield-imagery)

One day per Carrington rotation of [HelioField imagery](https://github.com/sr-dash/heliofield-imagery), back to May 2010: SDO/AIA and HMI, SOHO/LASCO, STEREO-A/EUVI and Solar Orbiter images with each observer's position, for [HelioField's Observations page](https://sr-dash.github.io/heliofield/observations.html).

The daily site keeps the last 60 days and is redeployed whenever a day is added. Older days live here, so they are not uploaded again with every daily deploy: each Monday the `Archive` workflow copies any day that has aged past the 60-day window (one per rotation) from the daily site's public files, and deploys this site only when it gained a day, about once a month.

```
https://sr-dash.github.io/heliofield-imagery-archive/index.json              the archived days and their rotations
https://sr-dash.github.io/heliofield-imagery-archive/days/<date>/index.json  that day's panels (as in the daily site)
https://sr-dash.github.io/heliofield-imagery-archive/days/<date>/<id>.std.webp, <id>.enh.webp
```

The daily site's `index.json` lists every date, with `archived` naming those served from here and `archive` giving this address, so readers find any date from one index. Images, methods and credits are described in [HelioField imagery](https://github.com/sr-dash/heliofield-imagery); please cite it ([doi:10.5281/zenodo.23935774](https://doi.org/10.5281/zenodo.23935774)) and credit the missions.

MIT licence (code). Made by [Soumyaranjan Dash](https://sr-dash.github.io/).

## Branches

- `main`: the code and workflows.
- `site`: the archived days and their index, as served. It is a single commit with no history, replaced whole by the workflow on each update, so the repository stays the size of what is on show instead of keeping every old file. It shares no history with `main` (GitHub calls them diverged) and is never merged into it; ignore any "Compare & pull request" banner for it.
