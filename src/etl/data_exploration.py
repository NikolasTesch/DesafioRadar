"""
Lembre-se de alterar a versão do Python para uma compatível com PyEnv - Recomendamos a 3.13.11 -
e de instalar as dependências com o Poetry e inicar o ambiente virtual antes de rodar este arquivo!
"""

import time
import pandas as pd
import argparse
from ydata_profiling import ProfileReport


def run_data_exploration(raw_data_path: str, output_report_path: str):
    print(f"Lendo dados de: {raw_data_path}")
    super_dataset = pd.read_csv(raw_data_path)
    
    print("Iniciando o YData Profiling Report...")
    start = time.perf_counter()
    profile_report = ProfileReport(
        super_dataset, 
        title="Olist Super Dataset Profiling Report",
        minimal=True # Para uma visualização mais completa, tem a opção de retirar esse parâmetro - Mas já aviso que demora bem...
    )
    profile_report.to_file(output_report_path)
    end = time.perf_counter() - start
    print(f"Relatório gerado em: {output_report_path}")
    print(f"Tempo de execução: {end:.2f} segundos")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Perfilamento de Dados (YData Profiling)")
    parser.add_argument("--raw", default="data/processed/olist_super_dataset.csv", help="Caminho para arquivo CSV limpo (base)")
    parser.add_argument("--out", default="data/processed/ydata_profiling.html", help="Caminho do relatório HTML de saída")
    args = parser.parse_args()

    run_data_exploration(args.raw, args.out)