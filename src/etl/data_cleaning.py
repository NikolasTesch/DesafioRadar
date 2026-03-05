import pandas as pd
import unidecode
import os

def clean_and_merge_data(raw_data_dir: str, output_path: str):
    """
    Executa o pipeline principal (ETL) sobre os datasets da Olist.
    
    Aplica técnicas de Early Drop O(1) e processamento vetorial para mitigar gargalos de RAM.
    Engenha features logísticas (SLA e atraso), higieniza localidades geográficas via unidecode 
    e opera uma desnormalização controlada focado no grão 'Item-Nível', fundindo tabelas satélites 
    após agregações isoladas para evitar duplicação 1:N de pagamentos e avaliações. 
    Aplica cortes rígidos em outliers numéricos de negócios.

    Args:
        raw_data_dir (str): Caminho raiz contendo as matrizes .csv originais.
        output_path (str): Destino do dump final com o Super Dataset consolidado.
        
    Returns:
        None (I/O em disco)
    """
    print("Iniciando Pipeline de Limpeza (ETL)...")

    # 1. Carregamento dos dados brutos
    print("1. Carregando dados...")
    orders = pd.read_csv(os.path.join(raw_data_dir, "olist_orders_dataset.csv"))
    items = pd.read_csv(os.path.join(raw_data_dir, "olist_order_items_dataset.csv"))
    customers = pd.read_csv(os.path.join(raw_data_dir, "olist_customers_dataset.csv"))
    payments = pd.read_csv(os.path.join(raw_data_dir, "olist_order_payments_dataset.csv"))
    reviews = pd.read_csv(os.path.join(raw_data_dir, "olist_order_reviews_dataset.csv"))
    products = pd.read_csv(os.path.join(raw_data_dir, "olist_products_dataset.csv"))
    sellers = pd.read_csv(os.path.join(raw_data_dir, "olist_sellers_dataset.csv"))

    # 2. Limpeza e Tratamento (Etapa 2)
    print("2. Aplicando Tratamentos de Limpeza...")

<<<<<<< Updated upstream
    # 2.1 - Filtro de Pedidos Válidos (Regra de Negócio 4.1 do PRD)
    # Considerar apenas 'delivered'
    valid_status = ["delivered"]
    orders = orders[orders['order_status'].isin(valid_status)].copy()

    # 2.2 - Conversão de Datas (Datetime)
    date_columns = [
        'order_purchase_timestamp', 'order_approved_at', 
        'order_delivered_carrier_date', 'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    for col in date_columns:
        orders[col] = pd.to_datetime(orders[col])
    
    # 2.3 - Limpeza de Strings (Ex: padronizar cidades dos clientes)
=======
    # Orders
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

    # Customers
>>>>>>> Stashed changes
    def clean_text(text):
        if pd.isna(text):
            return text
        return unidecode.unidecode(str(text).lower().strip())
    customers['customer_city'] = customers['customer_city'].apply(clean_text)

<<<<<<< Updated upstream
    # 2.4 - Tratamento de Nulos
    # Pedidos sem data de entrega real devem ser mantidos como NaT e excluídos do cálculo de média depois

    # 3. Engenharia de Recursos (Feature Engineering) (PRD 3.1)
    print("3. Criando novas colunas (Feature Engineering)...")

    # Tempo de Entrega (Dias corridos)
    orders['tempo_entrega_dias'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
    # Filtrar tempos de entrega válidos (maior que 0 e até 100 dias)
    orders = orders[
        (orders["tempo_entrega_dias"] > 0) & (orders["tempo_entrega_dias"] <= 100)
    ].copy()

    # Atraso na Entrega (Booleano)
    orders['atraso_entrega'] = orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date']

    # 4. Modelagem e Mesclagem (Joins) (Etapa 3 do PRD)
    print("4. Realizando Joins...")

    # 4.1 Join Traduções de Categoria
    products = products.merge(translators, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna('other')

    # Remover colunas indesejadas de produtos
    cols_to_drop = [
        "product_name_lenght",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    products = products.drop(columns=cols_to_drop, errors="ignore")
=======
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
>>>>>>> Stashed changes

    # 4.2 Super DataFrame (Base Fato = Orders)
    df_merged = orders.merge(customers, on='customer_id', how='left')
    df_merged = df_merged.merge(items, on='order_id', how='left')
    df_merged = df_merged.merge(products, on='product_id', how='left')
<<<<<<< Updated upstream
    
    # Adicionando Pagamentos (Groupby por order_id se houver múltiplos, ou merge direto)
    # Como um pedido pode ter múltiplos pagamentos, vamos somar o valor pago por pedido (GMV)
    payments_agg = payments.groupby('order_id', as_index=False)['payment_value'].sum()
=======
    df_merged = df_merged.merge(sellers, on='seller_id', how='left')
>>>>>>> Stashed changes
    df_merged = df_merged.merge(payments_agg, on='order_id', how='left')

    # Adicionando Reviews (Pegando apenas o review_score médio se houver mais de um)
    reviews_agg = reviews.groupby('order_id', as_index=False)['review_score'].mean()
    df_merged = df_merged.merge(reviews_agg, on='order_id', how='left')
<<<<<<< Updated upstream

    # Receita Líquida (Para detalhe de item a item)
=======
>>>>>>> Stashed changes
    df_merged['receita_liquida'] = df_merged['price'] + df_merged['freight_value']

    # 4.3 Tratamento de Outliers (Regras Fnanceiras)
    print("Filtrando Outliers Financeiros...")

    df_merged = df_merged[
        (df_merged["price"].isna() | (df_merged["price"] <= 2000))&
        (df_merged["freight_value"].isna() | (df_merged["freight_value"] <= 200))&
        (df_merged["payment_value"].isna() | (df_merged["payment_value"] <= 8000))
    ].copy()

    # 5. Salvando Super Dataset
    print(f"5. Exportando Dados Finais (Linhas: {len(df_merged)})...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_merged.to_csv(output_path, index=False)
    
    print(f"Limpeza finalizada com sucesso! O arquivo está salvo em: {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Script de Limpeza (ETL)")
    parser.add_argument("--raw", default="data/raw", help="Caminho para arquivos CSV brutos")
    parser.add_argument("--out", default="data/processed/olist_super_dataset.csv", help="Caminho de saída")
    args = parser.parse_args()

    clean_and_merge_data(args.raw, args.out)

