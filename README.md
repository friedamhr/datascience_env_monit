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

    
## Block 5 report: Are my tower years normal?

Source: `reports/block5_question.ipynb`

Python packages: `pandas numpy matplotlib rasterio requests cdsapi jupyter nbconvert ipykernel`

1. Put `tower_sets_block4.csv` (ILIAS, folder DATA) in the project folder.
2. Download the data (run from the project folder):

       python scripts/get_my_towers.py --student 17
       python scripts/block5/02_worldclim.py --student 17
       python scripts/block5/01_era5land.py --student 17

   ERA5-Land needs a Copernicus Climate Data Store account, the accepted ERA5-Land licence and a token in `~/.cdsapirc` (see the script header).
3. Render the report:

       jupyter nbconvert --to html --execute --ExecutePreprocessor.timeout=600 reports/block5_question.ipynb