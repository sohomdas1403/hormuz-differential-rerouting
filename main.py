from data_processor import build_panel
from regression import run_did, save_did_results, run_poisson, save_poisson_results

build_panel()

did_results = run_did()
save_did_results(did_results)

poisson_results = run_poisson()
save_poisson_results(poisson_results)