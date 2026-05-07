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
- pandas, openpyxl, statsmodels