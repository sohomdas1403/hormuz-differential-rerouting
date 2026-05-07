import pandas as pd
import statsmodels.formula.api as smf


def run_did():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    model = smf.ols("crossings ~ Post + Shadow_dummy + Post_X_Shadow", data=panel)
    results = model.fit()

    print(results.summary())
    return results


def save_did_results(results):
    table = pd.DataFrame({
        "Coefficient":  results.params,
        "Std. Error":   results.bse,
        "t-Statistic":  results.tvalues,
        "p-Value":      results.pvalues,
        "95% CI Lower": results.conf_int()[0],
        "95% CI Upper": results.conf_int()[1],
    })

    summary = pd.DataFrame({
        "Metric": ["R-squared", "Adj. R-squared", "F-statistic", "Prob (F-statistic)", "No. Observations"],
        "Value":  [results.rsquared, results.rsquared_adj, results.fvalue, results.f_pvalue, results.nobs],
    })

    with pd.ExcelWriter("hormuz_did_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)

    print("Saved hormuz_did_results.xlsx")


def run_poisson():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    model = smf.poisson("crossings ~ Post + Shadow_dummy + Post_X_Shadow", data=panel)
    results = model.fit()

    print(results.summary())
    return results


def save_poisson_results(results):
    import numpy as np

    table = pd.DataFrame({
        "Coefficient":  results.params,
        "Std. Error":   results.bse,
        "z-Statistic":  results.tvalues,
        "p-Value":      results.pvalues,
        "95% CI Lower": results.conf_int()[0],
        "95% CI Upper": results.conf_int()[1],
        "IRR (exp(coef))": np.exp(results.params),
    })

    summary = pd.DataFrame({
        "Metric": ["Log-Likelihood", "Pseudo R-squared", "LLR p-value", "No. Observations"],
        "Value":  [results.llf, results.prsquared, results.llr_pvalue, results.nobs],
    })

    with pd.ExcelWriter("hormuz_poisson_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)

    print("Saved hormuz_poisson_results.xlsx")