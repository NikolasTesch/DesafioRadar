"""
Observe que este arquivo difere do data_cleaning.py em relação ao tratamento de outliers;
Essa abordagem é dinamica, ou seja, os limites de outliers são calculados dinamicamente.

Para análises, considerar ambos os arquivos para uma análise mais completa.
"""

import pandas as pd
import unidecode
import argparse
import os

def clean_and_merge_data(raw_data_dir: str, output_path: str):
    """
    Executa o pipeline principal (ETL) sobre os datasets da Olist.
    
    Aplica técnicas de Early Drop O(1) e processamento vetorial para mitigar gargalos de RAM.
    Engenha features logísticas (SLA e atraso), higieniza localidades geográficas via unidecode 
    e opera uma desnormalização controlada focado no grão 'Item-Nível', fundindo tabelas satélites 
    após agregações isoladas para evitar duplicação 1:N de pagamentos e avaliações. 
    Aplica técnicas de ESTATÍSTICA ROBUSTA (IQR e Percentil Extremo) para filtrar transações anômalas (Outliers) dinamicamente, abandonando limites fixos.

    Args:
        raw_data_dir (str): Caminho raiz contendo as matrizes .csv originais.
        output_path (str): Destino do dump final com o Super Dataset consolidado.
        
    Returns:
        None (I/O em disco)
    """

    def clean_text(text):
        """
        Remove acentos, deixa em minúsculo e remove espaços em branco.
        """
        if pd.isna(text):
            return text
        return unidecode.unidecode(str(text).lower().strip())

    print("Iniciando Pipeline de Limpeza (ETL)...")

    print("1. Carregando dados...")

    orders = pd.read_csv(os.path.join(raw_data_dir, "olist_orders_dataset.csv"))
    items = pd.read_csv(os.path.join(raw_data_dir, "olist_order_items_dataset.csv"))
    customers = pd.read_csv(os.path.join(raw_data_dir, "olist_customers_dataset.csv"))
    payments = pd.read_csv(os.path.join(raw_data_dir, "olist_order_payments_dataset.csv"))
    reviews = pd.read_csv(os.path.join(raw_data_dir, "olist_order_reviews_dataset.csv"))
    products = pd.read_csv(os.path.join(raw_data_dir, "olist_products_dataset.csv"))
    sellers = pd.read_csv(os.path.join(raw_data_dir, "olist_sellers_dataset.csv"))

    print("2. Aplicando Tratamentos e Early Drops (Drop de Memória)...")

    # Orders
    orders = orders[orders['order_status'] == 'delivered'].copy()
    for col in ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
        orders[col] = pd.to_datetime(orders[col])
    orders['tempo_entrega_dias'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    orders['atraso_entrega'] = orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']
    q_995 = orders["tempo_entrega_dias"].quantile(0.995)
    orders = orders[
        (orders["tempo_entrega_dias"] > 0) & (orders["tempo_entrega_dias"] <= q_995) 
    ].copy()
    orders_cols_to_keep = ['order_id', 'customer_id', 'order_purchase_timestamp', 'order_delivered_customer_date', 'tempo_entrega_dias', 'atraso_entrega']
    orders = orders[orders_cols_to_keep]

    # Customers
    customers['customer_city'] = customers['customer_city'].apply(clean_text)
    customers_cols_to_keep = ['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']
    customers = customers[customers_cols_to_keep]

    # Sellers
    sellers['seller_city'] = sellers['seller_city'].apply(clean_text)
    sellers_cols_to_keep = ['seller_id', 'seller_city', 'seller_state']
    sellers = sellers[sellers_cols_to_keep]

    # Products
    products['product_category_name'] = products['product_category_name'].apply(clean_text).fillna('outros')
    products_cols_to_keep = ['product_id', 'product_category_name', 'product_photos_qty', 'product_description_lenght']
    products = products[products_cols_to_keep]

    # Items
    items_cols_to_keep = ['order_id', 'order_item_id', 'product_id', 'seller_id', 'price', 'freight_value']
    items = items[items_cols_to_keep]

    print("3. Realizando Pré-Agregações...")
    
    # Payments
    payments_agg = payments.groupby('order_id', as_index=False)['payment_value'].sum()
    
    # Reviews
    reviews_agg = reviews.groupby('order_id', as_index=False)['review_score'].mean()

    print("4. Executando Joins Otimizados...")

    df_merged = orders.merge(customers, on='customer_id', how='left')
    df_merged = df_merged.merge(items, on='order_id', how='inner')
    df_merged = df_merged.merge(products, on='product_id', how='left')
    df_merged = df_merged.merge(sellers, on='seller_id', how='left')
    df_merged = df_merged.merge(payments_agg, on='order_id', how='left')
    df_merged = df_merged.merge(reviews_agg, on='order_id', how='left')
    df_merged['receita_liquida'] = df_merged['price'] + df_merged['freight_value']
    
    print("Filtrando Outliers Financeiros...")

    # Função O(N) para Cauda Longa Extrema (Q3 + 3 * IQR)
    def calc_iqr_limit(df_col):
        q1 = df_col.quantile(0.25)
        q3 = df_col.quantile(0.75)
        iqr = q3 - q1
        return q3 + 3 * iqr

    limit_p = calc_iqr_limit(df_merged["price"])
    limit_f = calc_iqr_limit(df_merged["freight_value"])
    limit_v = calc_iqr_limit(df_merged["payment_value"])

    df_merged = df_merged[
        (df_merged["price"].isna() | (df_merged["price"] <= limit_p))&
        (df_merged["freight_value"].isna() | (df_merged["freight_value"] <= limit_f))&
        (df_merged["payment_value"].isna() | (df_merged["payment_value"] <= limit_v))
    ].copy()

    df_merged.dropna(axis=0, how='any', inplace=True)

    print(f"5. Exportando Dados Finais (Linhas: {len(df_merged)})...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_merged.to_csv(output_path, index=False)
    
    print(f"Limpeza finalizada com sucesso! O arquivo está salvo em: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Limpeza (ETL)")
    parser.add_argument("--raw", default="data/raw", help="Caminho para arquivos CSV brutos")
    parser.add_argument("--out", default="data/processed/olist_super_dataset_dynamic.csv", help="Caminho de saída")
    args = parser.parse_args()

    clean_and_merge_data(args.raw, args.out)