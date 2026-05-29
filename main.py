from data_processor import build_panel, build_summary_table
from regression import run_did, save_did_results, run_poisson, save_poisson_results, plot_did, run_nb, save_nb_results, save_combined_results

# Builds the balanced panel dataset with daily crossings by fleet type
# in preparation for regression analysis and computes variances 
# and means by group.

build_panel()
build_summary_table()

# Run DiD regression specification, save results, and plot fitted values

did_results = run_did()
save_did_results(did_results)
plot_did(did_results)

# Run Poisson regression specifications and save results.

poisson_results = run_poisson()
save_poisson_results(poisson_results)

# Run NB regression specification and save results.

nb_results = run_nb()
save_nb_results(nb_results)

# Build a single side-by-side regression table for all three specifications

save_combined_results(did_results, poisson_results, nb_results)