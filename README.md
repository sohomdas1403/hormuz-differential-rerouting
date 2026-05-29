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

## Environmental Analysis:
For the environmental proxy calculation, the data was treated through Excel. In the first page of the excel file called "Vessels passing Hormuz Strait EDITED with shadow (Environmental Analysis).xlsx" you will find the table with all the relevant information used in the project. From this data is possible to recover all the statistics presented in the report.