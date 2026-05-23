import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


def _stars(pvalues):
    return pvalues.map(lambda p: "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.1 else "")))


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
        "":             _stars(results.pvalues),
        "95% CI Lower": results.conf_int()[0],
        "95% CI Upper": results.conf_int()[1],
    })

    summary = pd.DataFrame({
        "Metric": ["R-squared", "Adj. R-squared", "F-statistic", "Prob (F-statistic)", "No. Observations"],
        "Value":  [results.rsquared, results.rsquared_adj, results.fvalue, results.f_pvalue, results.nobs],
    })

    note = pd.DataFrame({"Note": ["*** p<0.01   ** p<0.05   * p<0.1"]})

    with pd.ExcelWriter("hormuz_did_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)
        note.to_excel(writer, sheet_name="Coefficients", startrow=len(table) + 3, index=False, header=False)

    print("Saved hormuz_did_results.xlsx")


def run_poisson():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    model = smf.poisson("crossings ~ Post + Shadow_dummy + Post_X_Shadow", data=panel)
    results = model.fit()

    print(results.summary())
    return results


def save_poisson_results(results):
    table = pd.DataFrame({
        "Coefficient":     results.params,
        "Std. Error":      results.bse,
        "z-Statistic":     results.tvalues,
        "p-Value":         results.pvalues,
        "":                _stars(results.pvalues),
        "95% CI Lower":    results.conf_int()[0],
        "95% CI Upper":    results.conf_int()[1],
        "IRR (exp(coef))": np.exp(results.params),
    })

    summary = pd.DataFrame({
        "Metric": ["Log-Likelihood", "Pseudo R-squared", "LLR p-value", "No. Observations"],
        "Value":  [results.llf, results.prsquared, results.llr_pvalue, results.nobs],
    })

    irr = pd.DataFrame({
        "IRR":          np.exp(results.params),
        "95% CI Lower": np.exp(results.conf_int()[0]),
        "95% CI Upper": np.exp(results.conf_int()[1]),
        "":             _stars(results.pvalues),
    })

    note = pd.DataFrame({"Note": ["*** p<0.01   ** p<0.05   * p<0.1"]})

    with pd.ExcelWriter("hormuz_poisson_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)
        irr.to_excel(writer, sheet_name="IRR Table")
        note.to_excel(writer, sheet_name="Coefficients", startrow=len(table) + 3, index=False, header=False)
        note.to_excel(writer, sheet_name="IRR Table",    startrow=len(irr) + 3,   index=False, header=False)

    print("Saved hormuz_poisson_results.xlsx")


def run_nb():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    model = smf.negativebinomial("crossings ~ Post + Shadow_dummy + Post_X_Shadow", data=panel)
    results = model.fit()

    print(results.summary())
    return results


def save_nb_results(results):
    table = pd.DataFrame({
        "Coefficient":     results.params,
        "Std. Error":      results.bse,
        "z-Statistic":     results.tvalues,
        "p-Value":         results.pvalues,
        "":                _stars(results.pvalues),
        "95% CI Lower":    results.conf_int()[0],
        "95% CI Upper":    results.conf_int()[1],
        "IRR (exp(coef))": np.exp(results.params),
    })

    summary = pd.DataFrame({
        "Metric": ["Log-Likelihood", "Pseudo R-squared", "LLR p-value", "No. Observations"],
        "Value":  [results.llf, results.prsquared, results.llr_pvalue, results.nobs],
    })

    irr = pd.DataFrame({
        "IRR":          np.exp(results.params),
        "95% CI Lower": np.exp(results.conf_int()[0]),
        "95% CI Upper": np.exp(results.conf_int()[1]),
        "":             _stars(results.pvalues),
    })

    note = pd.DataFrame({"Note": ["*** p<0.01   ** p<0.05   * p<0.1"]})

    with pd.ExcelWriter("hormuz_nb_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)
        irr.to_excel(writer, sheet_name="IRR Table")
        note.to_excel(writer, sheet_name="Coefficients", startrow=len(table) + 3, index=False, header=False)
        note.to_excel(writer, sheet_name="IRR Table",    startrow=len(irr) + 3,   index=False, header=False)

    print("Saved hormuz_nb_results.xlsx")


def plot_did(results):
    panel = pd.read_excel("hormuz_did_panel.xlsx")
    panel["fitted"] = results.fittedvalues.values

    normal = panel[panel["Shadow_dummy"] == 0].sort_values("Date")
    shadow = panel[panel["Shadow_dummy"] == 1].sort_values("Date")

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(normal["Date"], normal["fitted"], color="black", linewidth=2, label="Normal fleet (fitted)")
    ax.plot(shadow["Date"], shadow["fitted"], color="blue",  linewidth=2, label="Shadow fleet (fitted)")
    ax.axvline(pd.Timestamp("2026-03-01"), color="red", linewidth=1.5, linestyle="--", label="Blockade (Mar 1)")

    label_date = pd.Timestamp("2026-03-08")
    ax.text(label_date, 14,  r"$\beta_1$ = -104.33 (-90.3%)",       color="black", fontsize=9, va="bottom")
    ax.text(label_date, 3.5, r"$\beta_1 + \beta_3$ = -3.1 (-63.3%)", color="blue",  fontsize=9, va="bottom")

    ax.set_xlabel("Date")
    ax.set_ylabel("Daily crossings (fitted)")
    ax.set_title("Difference-in-Differences: Strait of Hormuz Crossings")
    ax.legend()
    fig.tight_layout()

    fig.savefig("hormuz_did_plot.png", dpi=150)
    plt.close(fig)
    print("Saved hormuz_did_plot.png")