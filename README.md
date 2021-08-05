# Installation

```bash
git clone https://github.com/vozdeckyl/TIMTowerMeasurements.git
cd TIMTowerMeasurements
chmod +x fit_all.py fitting.py make_plots.py
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
```
Before each run you will need to activate the virtual environment
```bash
source venv/bin/activate
```

At the end you can deactivate the environment by running
```bash
deactivate
```

# Run

## Simple fit

For a simple single fit run
```bash
./fitting.py A40M-000231_box.csv
```
This will print the fit output on the screen and make some PNG plots.

## Fitting multiple measurements

In order to plot multiple measurements (e.g. measurements 248,249,250) saved in the `data` folder, use:
```bash
./fit_all.py -i 248 250 -o summary.csv -p plots data
```
The script will output the fit plots to the pre-existing `plots` folder as well as a summary CSV into the root directory.

The input files in the `data` folder have to be in the correct format: `A40M-000xxx_box.csv` and `A40M-000xxx_info.csv`.

For plotting a single measurement use
```bash
./fit_all.py -m 250 -o summary.csv -p plots data
```


