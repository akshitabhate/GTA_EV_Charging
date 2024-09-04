# GTA-EV-Infrastructure
A look at the EV infrastructure in the Greater Toronto Area

## Pre-requisities

This repository has been tested on an `M2 Macbook Pro` running `MacOS 14.6.1` and `Python 3.9.6`.

To install the pre-requisites, use the following commands:

```bash
python3 -m pip install -r requirements.txt
```

## Running the script

The script can be run using the following command:

```bash
cd prototype
python3 -m streamlit run test.py
```

## Data Sources

This dashboard uses the following datasets for visualization:

| Data | Source | Description |
|---|---|---|
| Toronto City | https://github.com/jasonicarter/toronto-geojson | Description of Greater Toronto Area |
| City installed EV Chargers | https://www.toronto.ca/services-payments/water-environment/environmentally-friendly-city-initiatives/reports-plans-policies-research/electric-vehicles/city-operated-ev-charging-stations-map/#location=&lat=&lng=&zoom= | Last refreshed July 25, 2024 |
| EV in Ontario | https://data.ontario.ca/dataset/electric-vehicles-in-ontario-by-forward-sortation-area | Data fron 1 Jan 2023 to 30 July 2024 |
| Toronto City by Postal Area | https://github.com/ag2816/Visualizations/tree/master/data | Geographic bounds of Toronto by Forward Sorting Areas (FSA) | 