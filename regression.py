import pandas as pd
import statsmodels.formula.api as smf


def run_did():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    model = smf.ols("crossings ~ Post + Shadow_dummy + Post_X_Shadow", data=panel)
    results = model.fit()

    print(results.summary())
    return results