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
    """Orquestra a análise exploratória de dados (EDA) automática sobre os datasets processados.

    Gera dois relatórios do YData Profiling (HTML) para permitir a auditoria
    das distribuições e correlações entre o dataset bruto e o dataset limpo.

    Returns:
        None: Os relatórios são salvos diretamente em disco.
    """
    merged_data_path = "data/processed/olist_ALL_RAW_MERGED.csv"
    cleaned_data_path = "data/processed/olist_cleaned_dataset.csv"

    output_report_merged = "data/processed/profiling_merged_raw.html"
    output_report_cleaned = "data/processed/profiling_cleaned_dataset.html"

    for file_path in [merged_data_path, cleaned_data_path]:
        if not os.path.exists(file_path):
            print(f"[ERRO] Arquivo não localizado: '{file_path}'")
            sys.exit(1)

    print(f"Lendo {merged_data_path}...")
    df_merged = pd.read_csv(merged_data_path)

    # Perfil 1: Dados Brutos Unidos
    print("\nGerando perfil para: Dados Brutos Unidos...")
    start = time.perf_counter()
    ProfileReport(
        df_merged, title="Olist Merged Raw Data Profiling", minimal=True
    ).to_file(output_report_merged)
    print(f"Concluído em: {time.perf_counter() - start:.2f}s -> {output_report_merged}")

    print(f"\nLendo {cleaned_data_path}...")
    df_cleaned = pd.read_csv(cleaned_data_path)

    # Perfil 2: Dados Limpos e Tratados
    print("\nGerando perfil para: Dados Limpos e Tratados...")
    start = time.perf_counter()
    ProfileReport(
        df_cleaned, title="Olist Cleaned Dataset Profiling", minimal=True
    ).to_file(output_report_cleaned)
    print(
        f"Concluído em: {time.perf_counter() - start:.2f}s -> {output_report_cleaned}"
    )

if __name__ == "__main__":
    run_data_exploration()