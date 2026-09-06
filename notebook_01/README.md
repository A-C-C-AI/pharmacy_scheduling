# Notebook 01

Open `01_baseline_schedule_analysis_v2.ipynb` to read the executed notebook. Each code cell has one title; executable logic is unchanged from the verified project.

Run this notebook independently from its supplied inputs:

```bash
python run_notebook.py
```

Install the root requirements first. The launcher assembles the original relative paths in a temporary working directory, executes the actual cells and updates this notebook and `outputs/`. It does not change the model or notebook code. To run interactively, create a local working folder and use `prepare(folder, work)` from `run_notebook.py` to assemble it, then open the copied notebook in that working folder.

`inputs/` contains the required support modules, original CSV and all earlier-stage artifacts used by the transitive lineage checks. `inputs/provenance/` contains source-only snapshots of earlier notebooks so those checks can verify their sources. Repeated files are exact copies of earlier outputs. These snapshots are sufficient to run this stage without opening another notebook folder.

`outputs/` contains this stage's produced files:

- `baseline_evidence.json`
- `baseline_evidence.csv`
- `baseline_pharmacy_profile.csv`
- `stage_01_manifest.json`

Plots displayed by the notebook, where present, are also extracted under `outputs/plots/`; their values are unchanged. To rerun the whole pipeline and refresh downstream snapshots, use the root `run_project.py`.
