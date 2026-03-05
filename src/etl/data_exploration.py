"""
Lembre-se de alterar a versão do Python para uma compatível com PyEnv - Recomendamos a 3.13.11 -
e de instalar as dependências com o Poetry e inicar o ambiente virtual antes de rodar este arquivo!
"""

import os
import sys
import time
import pandas as pd
from ydata_profiling import ProfileReport


def run_data_exploration():
    """
    Orquestra a análise exploratória de dados (EDA) automática sobre os pipelines de ETL.
    
    Injeta um Gatekeeper (validação de I/O) para abortar a thread caso as tabelas-fato 
    Estática e Dinâmica não tenham sido consolidadas. Omitido isso, instiga dois fluxos 
    do YData Profiling para gerar sumários descritivos rigorosos e renderiza snapshots 
    (HTML) permitindo auditoria das distribuições tratadas versus cruas.

    Returns:
        None (I/O em disco)
    """
    raw_data_path = "data/processed/olist_super_dataset.csv"
    raw_data_path_dynamic = "data/processed/olist_super_dataset_dynamic.csv"
    output_report_path = "data/processed/ydata_profiling.html"
    output_report_path_dynamic = "data/processed/ydata_profiling_dynamic.html"
    
    for file_path in [raw_data_path, raw_data_path_dynamic]:
        if not os.path.exists(file_path):
            print(f"[ERRO ARQUITETURAL] Falha de Dependência: '{file_path}' não localizado.")
            print("A esteira de exploração exige que a Limpeza de Dados tenha sido efetuada.")
            print("Execute previamente os passos geradores:")
            print(" 1 -> poetry run python src/etl/data_cleaning.py")
            print(" 2 -> poetry run python src/etl/data_cleaning_dynamic.py")
            sys.exit(1)

    super_dataset = pd.read_csv(raw_data_path)
    super_dataset_dynamic = pd.read_csv(raw_data_path_dynamic)
    
    start = time.perf_counter()
    profile_report = ProfileReport(
        super_dataset, 
        title="Olist Super Dataset Profiling Report",
        minimal=True # Para uma visualização mais completa, tem a opção de retirar esse parâmetro - Mas já aviso que demora bem...
    )
    profile_report.to_file(output_report_path)
    end = time.perf_counter() - start
    print(f"Tempo de execução: {end:.2f} segundos\nLocal: {output_report_path}")

    start = time.perf_counter()
    profile_report_dynamic = ProfileReport(
        super_dataset_dynamic, 
        title="Olist Super Dataset Profiling Report Dynamic",
        minimal=True # Para uma visualização mais completa, tem a opção de retirar esse parâmetro - Mas já aviso que demora bem...
    )
    profile_report_dynamic.to_file(output_report_path_dynamic)
    end = time.perf_counter() - start
    print(f"Tempo de execução: {end:.2f} segundos\nLocal: {output_report_path_dynamic}")

if __name__ == "__main__":
    run_data_exploration()