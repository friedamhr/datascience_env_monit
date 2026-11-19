# Cluster hello
Bootstraps a synthetic GPP series and prints a 95 % interval.

## How do I run it?
python3 scripts/cluster_hello.py 200

## What is in the folder?
scripts/ the analysis code
jobs/ Slurm job scripts
docs/ notes and templates
.gitignore

## Author
Frieda Mohr 05.11.2026

## Block 4 report
Requires the five FLUXNET zips in `data/raw` (download with `python3 scripts/get_my_towers.py --student 17`).
Render with:
    jupyter nbconvert --to html --execute --ExecutePreprocessor.timeout=600 reports/block4_data_summary.ipynb