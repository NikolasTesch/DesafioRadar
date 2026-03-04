"""
Lembre-se de alterar a versão do Python para uma compatível com PyEnv - Recomendamos a 3.13.11 -
e de instalar as dependências com o Poetry e inicar o ambiente virtual antes de rodar este arquivo!
"""

import time
import pandas as pd
from ydata_profiling import ProfileReport


def run_data_exploration():
    raw_data_path = "data/processed/olist_super_dataset.csv"
    output_report_path = "data/processed/ydata_profiling.html"
    
    super_dataset = pd.read_csv(raw_data_path)
    
    start = time.perf_counter()
    profile_report = ProfileReport(
        super_dataset, 
        title="Olist Super Dataset Profiling Report",
        minimal=True # Para uma visualização mais completa, tem a opção de retirar esse parâmetro - Mas já aviso que demora bem...
    )
    profile_report.to_file(output_report_path)
    end = time.perf_counter() - start
    print(f"Tempo de execução: {end:.2f} segundos")

run_data_exploration()