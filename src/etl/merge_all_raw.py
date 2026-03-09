import pandas as pd
import os
import argparse

def merge_all_raw_data(raw_data_dir: str, output_path: str):
    """Lê todos os CSVs principais da Olist e realiza a união em um único CSV master.

    Args:
        raw_data_dir (str): Caminho para o diretório contendo os arquivos CSV brutos.
        output_path (str): Caminho completo onde o arquivo CSV master será salvo.

    Returns:
        None: O resultado é salvo diretamente em disco.
    """
    print(f"Iniciando a leitura dos arquivos brutos na pasta: {raw_data_dir} ...")

    # Carregando Datasets
    try:
        orders = pd.read_csv(os.path.join(raw_data_dir, "olist_orders_dataset.csv"))
        items = pd.read_csv(os.path.join(raw_data_dir, "olist_order_items_dataset.csv"))
        products = pd.read_csv(os.path.join(raw_data_dir, "olist_products_dataset.csv"))
        customers = pd.read_csv(os.path.join(raw_data_dir, "olist_customers_dataset.csv"))
        sellers = pd.read_csv(os.path.join(raw_data_dir, "olist_sellers_dataset.csv"))
        payments = pd.read_csv(os.path.join(raw_data_dir, "olist_order_payments_dataset.csv"))
        reviews = pd.read_csv(os.path.join(raw_data_dir, "olist_order_reviews_dataset.csv"))
        geolocation = pd.read_csv(os.path.join(raw_data_dir, "olist_geolocation_dataset.csv"))
        category_translation = pd.read_csv(os.path.join(raw_data_dir, "product_category_name_translation.csv"))
    except FileNotFoundError as e:
        print(f"Erro: Arquivo bruto não encontrado na pasta raw: {e}")
        return

    print("Todos os CSVs carregados para a RAM com sucesso.")
    print("Iniciando a união (Merge) das tabelas relacionais em memória...")
    df_merged = orders.merge(items, on='order_id', how='inner')
    df_merged = df_merged.merge(products, on='product_id', how='left')
    df_merged = df_merged.merge(category_translation, on='product_category_name', how='left')
    df_merged = df_merged.merge(customers, on='customer_id', how='left')
    df_merged = df_merged.merge(sellers, on='seller_id', how='left')
    payments_agg = payments.groupby('order_id', as_index=False)['payment_value'].sum()
    df_merged = df_merged.merge(payments_agg, on='order_id', how='left')

    reviews_agg = reviews.groupby('order_id', as_index=False).agg({
        'review_score': 'mean',
        'review_comment_message': 'last'
    })
    df_merged = df_merged.merge(reviews_agg, on='order_id', how='left')

    geo_group = geolocation.groupby('geolocation_zip_code_prefix').agg({
        'geolocation_lat': 'median',
        'geolocation_lng': 'median'
    }).reset_index()
    
    df_merged = df_merged.merge(geo_group, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
    df_merged.rename(columns={'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'}, inplace=True)
    df_merged.drop('geolocation_zip_code_prefix', axis=1, inplace=True, errors='ignore')

    df_merged = df_merged.merge(geo_group, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
    df_merged.rename(columns={'geolocation_lat': 'seller_lat', 'geolocation_lng': 'seller_lng'}, inplace=True)
    df_merged.drop('geolocation_zip_code_prefix', axis=1, inplace=True, errors='ignore')

    print(f"Merge finalizado. O dataset mestre gerado possui {df_merged.shape[0]} linhas e {df_merged.shape[1]} colunas.")
    print(f"Exportando o tabelão desnormalizado para: {output_path} (Isso pode demorar dependendo do seu disco)...")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salva o arquivo CSV master
    df_merged.to_csv(output_path, index=False)
    
    print("Sucesso absoluto! Script finalizado. Seu arquivo CSV Mestre aguarda leitura.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para juntar todos os arquivos Brutos em 1 CSV")
    # Valores default genéricos baseados na raiz do projeto
    default_raw = os.path.join("data", "raw")
    default_out = os.path.join("data", "processed", "olist_ALL_RAW_MERGED.csv")
    
    parser.add_argument("--raw", default=default_raw, help="Pasta contendo todos os arquivos raw .csv originais da olist")
    parser.add_argument("--out", default=default_out, help="Caminho do arquivo desnormalizado único (master csv)")
    
    args = parser.parse_args()

    merge_all_raw_data(args.raw, args.out)
