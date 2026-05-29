## Setup — Create environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# On Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (to avoid Microsoft Store Python Path Issues):
python -m pip install -r requirements.txt
```

## Usage:
```bash
python main.py
```

## Requirements
- Python 3.10.11
- venv
- numpy, pandas, openpyxl, matplotlib, statsmodels

## Project Structure:

The analysis is split across three Python files. Running `main.py` executes the full pipeline from raw data to outputs.

**`data_processor.py`**
Reads the raw vessel-level dataset (`Vessels passing Hormuz Strait EDITED with shadow.xlsx`), extracts the variables of interest, and compiles them into a balanced panel suitable for regression. Each date appears twice (once for each fleet type), with every observation including daily crossing counts, a post-treatment dummy (for before/after the geopolitical shock on March 1), and a fleet-type dummy. Also produces a descriptive summary table of means and variances by group. Outputs: `hormuz_did_panel.xlsx`, `hormuz_summary_table.xlsx`.

**`regression.py`**
Runs the three regression specifications on the panel (DiD, Poisson, and Negative Binomial) and handles all result output. Each specification has a dedicated run function and a dedicated save function. Results are written to individual Excel files (.xlsx) with coefficient tables, model fit statistics, and significance stars. A combined side-by-side table is also produced for easy comparison across specifications (for the report and presentation). Also generates the DiD visualisation using its fitted values. Outputs: `hormuz_did_results.xlsx`, `hormuz_poisson_results.xlsx`, `hormuz_nb_results.xlsx`, `hormuz_combined_results.xlsx`, `hormuz_did_plot.png`.

**`main.py`**
Entry point. Calls each function from `data_processor.py` and `regression.py` in the correct order: build panel, produce summary table, run each regression, save results, and build the combined table from the produced results. Running `python main.py` reproduces all outputs from scratch.


## Environmental Analysis:
For the environmental proxy calculation, the data was treated through Excel. In the first page of the excel file called "Environmental Analysis.xlsx" you will find the table with all the relevant information used in the project. From this data is possible to recover all the statistics presented in the report.