import zipfile
from pathlib import Path
import pandas as pd

KEEP = ["TIMESTAMP_START", "TIMESTAMP_END", "TA_F", "SW_IN_F", "VPD_F", "P_F",
        "NETRAD", "G_F_MDS", "H_F_MDS", "H_F_MDS_QC", "LE_F_MDS", "LE_F_MDS_QC",
        "NEE_VUT_REF", "NEE_VUT_REF_QC", "GPP_NT_VUT_REF", "RECO_NT_VUT_REF"]


def read_hh(zip_file):
    """Liest die FLUXMET_HH-Datei aus einem FLUXNET-Zip und gibt eine Tabelle mit Spalte 'site' zurück."""
    zip_file = Path(zip_file)
    site = zip_file.name.split("_")[1]          # z. B. AMF_US-ChR_... -> US-ChR

    with zipfile.ZipFile(zip_file) as z:
        hh_name = [n for n in z.namelist() if "FLUXMET_HH" in n][0]
        with z.open(hh_name) as f:
            hh = pd.read_csv(f, na_values=[-9999],
                             usecols=lambda c: c in KEEP,
                             dtype={"TIMESTAMP_START": str, "TIMESTAMP_END": str})

    hh["time"] = pd.to_datetime(hh["TIMESTAMP_START"], format="%Y%m%d%H%M")
    hh.insert(0, "site", site)
    return hh


def read_all(raw_dir="data/raw"):
    """Liest alle Zips in raw_dir und hängt sie zu einer Tabelle zusammen."""
    zips = sorted(Path(raw_dir).glob("*.zip"))
    return pd.concat([read_hh(z) for z in zips], ignore_index=True)


if __name__ == "__main__":
    flux = read_all()

    # Überblick pro Turm
    overview = flux.groupby("site").agg(
        rows=("time", "size"),
        start=("time", "min"),
        end=("time", "max"),
        nee_measured=("NEE_VUT_REF_QC", lambda q: (q == 0).mean()),
    )
    # Erwartete Zeilen, wenn jede halbe Stunde genau einmal vorkommt
    overview["expected"] = ((overview["end"] - overview["start"]) / pd.Timedelta("30min") + 1).astype(int)
    print(overview, "\n")

    print("Doppelte Zeitstempel (site + time):", flux.duplicated(["site", "time"]).sum(), "\n")

    # Welche Variablen fehlen bei welchem Turm komplett?
    for site, g in flux.groupby("site"):
        missing = [c for c in KEEP if g[c].isna().all()]
        print(f"{site}: komplett fehlend -> {missing if missing else 'nichts'}")