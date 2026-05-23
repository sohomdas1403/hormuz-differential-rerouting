import pandas as pd


def build_panel():
    df = pd.read_excel("Vessels passing Hormuz Strait EDITED with shadow.xlsx")

    all_dates = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
    skeleton = pd.MultiIndex.from_product([all_dates, [0, 1]], names=["Date", "Shadow_dummy"])
    skeleton = pd.DataFrame(index=skeleton).reset_index()

    crossings = (
        df.groupby(["Date", "Shadow"])
        .size()
        .reset_index(name="crossings")
        .rename(columns={"Shadow": "Shadow_dummy"})
    )

    panel = skeleton.merge(crossings, on=["Date", "Shadow_dummy"], how="left")
    panel["crossings"] = panel["crossings"].fillna(0).astype(int)
    panel["Post"] = (panel["Date"] >= "2026-03-01").astype(int)
    panel["Post_X_Shadow"] = panel["Post"] * panel["Shadow_dummy"]
    panel = panel[["Date", "Post", "Shadow_dummy", "crossings", "Post_X_Shadow"]]
    panel.sort_values(["Date", "Shadow_dummy"], inplace=True)
    panel.reset_index(drop=True, inplace=True)

    panel.to_excel("hormuz_did_panel.xlsx", index=False)
    print(f"Saved hormuz_did_panel.xlsx — {len(panel)} rows, {panel['Date'].nunique()} dates")


def build_summary_table():
    panel = pd.read_excel("hormuz_did_panel.xlsx")

    groups = {
        "Normal fleet — Pre":  (panel["Shadow_dummy"] == 0) & (panel["Post"] == 0),
        "Normal fleet — Post": (panel["Shadow_dummy"] == 0) & (panel["Post"] == 1),
        "Shadow fleet — Pre":  (panel["Shadow_dummy"] == 1) & (panel["Post"] == 0),
        "Shadow fleet — Post": (panel["Shadow_dummy"] == 1) & (panel["Post"] == 1),
    }

    rows = []
    for label, mask in groups.items():
        mean = panel.loc[mask, "crossings"].mean()
        var  = panel.loc[mask, "crossings"].var()
        rows.append({"Group": label, "Mean": mean, "Variance": var, "Ratio (Var / Mean)": var / mean})

    table = pd.DataFrame(rows)
    table.to_excel("hormuz_summary_table.xlsx", index=False)
    print("Saved hormuz_summary_table.xlsx")