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

    note = pd.DataFrame({"Note": ["*** p<0.01   ** p<0.05   * p<0.1"]})

    with pd.ExcelWriter("hormuz_poisson_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)
        note.to_excel(writer, sheet_name="Coefficients", startrow=len(table) + 3, index=False, header=False)

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
        "IRR (exp(coef))": np.where(results.params.index == "alpha", "—", np.exp(results.params)),
    })

    summary = pd.DataFrame({
        "Metric": ["Log-Likelihood", "Pseudo R-squared", "LLR p-value", "No. Observations"],
        "Value":  [results.llf, results.prsquared, results.llr_pvalue, results.nobs],
    })

    note = pd.DataFrame({"Note": ["*** p<0.01   ** p<0.05   * p<0.1"]})

    with pd.ExcelWriter("hormuz_nb_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Coefficients")
        summary.to_excel(writer, sheet_name="Model Summary", index=False)
        note.to_excel(writer, sheet_name="Coefficients", startrow=len(table) + 3, index=False, header=False)

    print("Saved hormuz_nb_results.xlsx")


def save_combined_results(did, poisson, nb):
    em = "—"

    def stars(pval):
        return "***" if pval < 0.01 else ("**" if pval < 0.05 else ("*" if pval < 0.1 else ""))

    def fmt(val, pval):
        return f"{val:.4f}{stars(pval)}"

    def fmt_se(val):
        return f"({val:.4f})"

    def fmt_irr(results, param):
        return f"{np.exp(results.params[param]):.4f}{stars(results.pvalues[param])}"

    rows = []

    def coef_rows(label, param, did_r=did, poi_r=poisson, nb_r=nb):
        rows.append({
            "": label,
            "DiD (OLS)":        fmt(did_r.params[param],    did_r.pvalues[param]),
            "Poisson":          fmt(poi_r.params[param],    poi_r.pvalues[param]),
            "Negative Binomial": fmt(nb_r.params[param],   nb_r.pvalues[param]),
        })
        rows.append({
            "": "",
            "DiD (OLS)":        fmt_se(did_r.bse[param]),
            "Poisson":          fmt_se(poi_r.bse[param]),
            "Negative Binomial": fmt_se(nb_r.bse[param]),
        })

    def irr_row(label, param):
        rows.append({
            "": label,
            "DiD (OLS)":        em,
            "Poisson":          fmt_irr(poisson, param),
            "Negative Binomial": fmt_irr(nb, param),
        })

    coef_rows("Intercept",    "Intercept")
    irr_row("IRR(Intercept)", "Intercept")
    coef_rows("Post",         "Post")
    irr_row("IRR(Post)",      "Post")
    coef_rows("Shadow",       "Shadow_dummy")
    irr_row("IRR(Shadow)",    "Shadow_dummy")
    coef_rows("Post x Shadow","Post_X_Shadow")
    irr_row("IRR(Post x Shadow)", "Post_X_Shadow")

    rows.append({
        "": "Dispersion (alpha)",
        "DiD (OLS)":        em,
        "Poisson":          em,
        "Negative Binomial": fmt(nb.params["alpha"], nb.pvalues["alpha"]),
    })
    rows.append({
        "": "",
        "DiD (OLS)":        em,
        "Poisson":          em,
        "Negative Binomial": fmt_se(nb.bse["alpha"]),
    })

    rows.append({"": "N",         "DiD (OLS)": int(did.nobs),         "Poisson": int(poisson.nobs),      "Negative Binomial": int(nb.nobs)})
    rows.append({"": "R²",        "DiD (OLS)": f"{did.rsquared:.4f}", "Poisson": em,                     "Negative Binomial": em})
    rows.append({"": "Pseudo R²", "DiD (OLS)": em,                    "Poisson": f"{poisson.prsquared:.4f}", "Negative Binomial": f"{nb.prsquared:.4f}"})

    table = pd.DataFrame(rows)

    with pd.ExcelWriter("hormuz_combined_results.xlsx", engine="openpyxl") as writer:
        table.to_excel(writer, sheet_name="Combined Results", index=False)
        note_row = len(table) + 2
        writer.sheets["Combined Results"].cell(row=note_row + 1, column=1, value="*** p<0.01   ** p<0.05   * p<0.1")

    print("Saved hormuz_combined_results.xlsx")


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