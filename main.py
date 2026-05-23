from data_processor import build_panel, build_summary_table
from regression import run_did, save_did_results, run_poisson, save_poisson_results, plot_did, run_nb, save_nb_results

build_panel()
build_summary_table()

did_results = run_did()
save_did_results(did_results)
plot_did(did_results)

poisson_results = run_poisson()
save_poisson_results(poisson_results)

nb_results = run_nb()
save_nb_results(nb_results)