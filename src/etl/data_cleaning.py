import pandas as pd
import unidecode
import os
import argparse

def clean_and_merge_data(raw_data_dir: str, output_path: str):
    """
    Executa a Etapa 1, 2 e 3 do PRD: Ingestão, Limpeza e Mesclagem de dados da Olist.
    """
    print("Iniciando Pipeline de Limpeza (ETL)...")

    print("1. Carregando dados...")
    orders = pd.read_csv(os.path.join(raw_data_dir, "olist_orders_dataset.csv"))
    items = pd.read_csv(os.path.join(raw_data_dir, "olist_order_items_dataset.csv"))
    customers = pd.read_csv(os.path.join(raw_data_dir, "olist_customers_dataset.csv"))
    payments = pd.read_csv(os.path.join(raw_data_dir, "olist_order_payments_dataset.csv"))
    reviews = pd.read_csv(os.path.join(raw_data_dir, "olist_order_reviews_dataset.csv"))
    products = pd.read_csv(os.path.join(raw_data_dir, "olist_products_dataset.csv"))
    translators = pd.read_csv(os.path.join(raw_data_dir, "product_category_name_translation.csv"))

    print("2. Aplicando Tratamentos e Early Drops (Drop de Memória)...")

    orders = orders[orders['order_status'] == 'delivered'].copy()
    
    for col in ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
        orders[col] = pd.to_datetime(orders[col])
        
    orders['tempo_entrega_dias'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    orders['atraso_entrega'] = orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']
    
    orders = orders[
        (orders["tempo_entrega_dias"] > 0) & (orders["tempo_entrega_dias"] <= 100)
    ].copy()

    orders_cols_to_keep = ['order_id', 'customer_id', 'order_purchase_timestamp', 'order_delivered_customer_date', 'tempo_entrega_dias', 'atraso_entrega']
    orders = orders[orders_cols_to_keep]

    def clean_text(text):
        if pd.isna(text):
            return text
        return unidecode.unidecode(str(text).lower().strip())
    
    customers['customer_city'] = customers['customer_city'].apply(clean_text)
    customers_cols_to_keep = ['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']
    customers = customers[customers_cols_to_keep]

    products = products.merge(translators, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna('other')
    products_cols_to_keep = ['product_id', 'product_category_name_english', 'product_photos_qty', 'product_description_lenght']
    products = products[products_cols_to_keep]

    items_cols_to_keep = ['order_id', 'order_item_id', 'product_id', 'seller_id', 'price', 'freight_value']
    items = items[items_cols_to_keep]

    print("3. Realizando Pré-Agregações...")
    
    payments_agg = payments.groupby('order_id', as_index=False)['payment_value'].sum()
    reviews_agg = reviews.groupby('order_id', as_index=False)['review_score'].mean()

    print("4. Executando Joins Otimizados...")

    df_merged = orders.merge(customers, on='customer_id', how='left')
    df_merged = df_merged.merge(items, on='order_id', how='inner')
    df_merged = df_merged.merge(products, on='product_id', how='left')
    df_merged = df_merged.merge(payments_agg, on='order_id', how='left')
    df_merged = df_merged.merge(reviews_agg, on='order_id', how='left')

    df_merged['receita_liquida'] = df_merged['price'] + df_merged['freight_value']

    print("Filtrando Outliers Financeiros...")
    df_merged = df_merged[
        (df_merged["price"].isna() | (df_merged["price"] <= 2000))
        & (df_merged["freight_value"].isna() | (df_merged["freight_value"] <= 200))
        & (df_merged["payment_value"].isna() | (df_merged["payment_value"] <= 8000))
    ].copy()

    df_merged.dropna(axis=0, how='any', inplace=True)

    print(f"5. Exportando Dados Finais (Linhas: {len(df_merged)})...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_merged.to_csv(output_path, index=False)
    
    print("Limpeza finalizada com sucesso! O arquivo está salvo em:")
    print(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Limpeza (ETL)")
    parser.add_argument("--raw", default="data/raw", help="Caminho para arquivos CSV brutos")
    parser.add_argument("--out", default="data/processed/olist_super_dataset.csv", help="Caminho de saída")
    args = parser.parse_args()

    clean_and_merge_data(args.raw, args.out)