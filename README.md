# Pharmacy Scheduling

This repository contains six executed notebooks for the pharmacy scheduling analysis, their frozen inputs and generated outputs, pinned Python dependencies, and the compiled final report.

## Reproduce all notebook results from the original CSV

Use Python 3.12 in a fresh clone or working copy:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install the dependencies and run the pipeline:

```bash
python -m pip install -r requirements.txt
python run_project.py
```

`run_project.py` starts with the original CSV in `notebook_00/inputs/data/`, executes notebooks 00 through 05 in order, and refreshes each downstream input snapshot from the outputs just produced. It updates the executed notebooks, stage outputs, manifests, provenance snapshots, and extracted figures in the working copy.

The compiled PDF is supplied as `report__1_ (1).pdf`. The notebook pipeline does not rebuild the PDF because the report-building sources are not part of this repository.

## Run one notebook independently

Every notebook folder is self-contained. For example:

```bash
python notebook_03/run_notebook.py
```

Replace `03` with a stage number from `00` to `05`. An independent run uses that folder's supplied frozen input snapshot and refreshes its executed notebook and `outputs/` directory.

## Repository contents

- `notebook_00/` through `notebook_05/`: executed notebooks, frozen inputs, outputs, manifests, and per-stage launchers
- `run_project.py`: sequential CSV-to-stage-05 pipeline launcher
- `requirements.txt`: pinned dependencies tested with Python 3.12
- `report__1_ (1).pdf`: compiled final report
