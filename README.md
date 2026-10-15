## Abstract:

This paper investigates whether geopolitical shocks to maritime chokepoints generate differential behavioural and environmental consequences for shadow and conventional merchant fleets. Exploiting the March 2026 Strait of Hormuz closure as a natural experiment, we apply a difference-in-differences (DiD) framework to vessel-level AIS tracking data to identify the causal effect of an acute geopolitical shock on crossing behaviour across fleet types. We document that the blockade reduced daily Strait crossings by 90.3% for conventional fleet vessels but only 63.3% for shadow fleet operators — a differential driven by the institutional asymmetry between the two groups: conventional vessels face binding war risk insurance constraints that shadow operators, excluded from regulated maritime frameworks, simply do not share. Beyond the crossing differential, we show that shadow fleet vessels carry a structurally higher emissions intensity: a mean annual CO2 proxy of 26,939 tonnes per vessel against 23,796 for conventional vessels, a 13.2% premium driven by older technology vintages and concentration in tanker and chemical-oil carrier segments. The combination of differential crossing resilience and higher per-vessel emissions intensity means that shadow vessels — representing 5.3% of unique vessels in the sample– account for a disproportionate 5.9% of implied aggregate annual emissions exposure, a share that grows post-closure as shadow vessels constitute an increasing fraction of active crossings. These findings illuminate a structural coherence failure at the intersection of sanctions regimes and maritime climate policy: the institutional mechanisms designed to constrain shadow fleet operations simultaneously insulate their operators from the disruptions those mechanisms generate, with material and widening environmental consequences precisely when geopolitical tensions are highest. We further expand the consideration to potential future shocks and re-routing of regulated fleets, leaving shadow fleets with a resilience and emissions comparative advantage.

**Keywords:** shadow fleet, environmental economics, maritime emissions, Strait of Hormuz, difference-in-differences, sanctions

## Attribution:
Group project for "Environmental Economics" course at the University of Lausanne, with Jules David, Tomas Delgado Ayala, Azizbek Makhmudjonov, and Eduardo Beltrao. "Environmental Analysis.xlsx" analysis was done mainly by Tomas Delgado Ayala. All python coding was done by the owner of the repository, Sohom Das. 

Grade Received: 6/6

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
For the environmental proxy calculation, the data was treated through Excel. In the excel file called "Environmental Analysis.xlsx" you will find all the relevant information used in the project. From this data is possible to recover all the statistics presented in the report. Further details are provided in the first sheet of the excel file called "Overview". 
