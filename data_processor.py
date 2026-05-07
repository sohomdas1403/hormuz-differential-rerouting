import pandas as pd

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