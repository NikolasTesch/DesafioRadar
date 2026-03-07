import streamlit as st
import pandas as pd
import os

# Configuração de caminhos
DATA_PATH = "data/raw/"

@st.cache_data
def load_data(file_name):
    """Carrega dados da pasta raw com cache do Streamlit."""
    path = os.path.join(DATA_PATH, file_name)
    if not os.path.exists(path):
        st.error(f"Arquivo não encontrado: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data
def treat_outliers_iqr(df, column):
    """Remove outliers usando a regra do Intervalo Interquartil (IQR)."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

@st.cache_data
def get_analytical_df():
    """Consolida a base analítica principal com métricas financeiras e logísticas."""
    df_orders = load_data("olist_orders_dataset.csv")
    df_customers = load_data("olist_customers_dataset.csv")
    df_items = load_data("olist_order_items_dataset.csv")
    df_products = load_data("olist_products_dataset.csv")
    df_sellers = load_data("olist_sellers_dataset.csv")
    df_reviews = load_data("olist_order_reviews_dataset.csv")
    df_payments = load_data("olist_order_payments_dataset.csv")

    if df_orders.empty:
        return pd.DataFrame()

    # Merge estrutural
    df = pd.merge(df_orders, df_customers, on="customer_id", how="inner")
    df = pd.merge(df, df_items, on="order_id", how="inner")
    df = pd.merge(df, df_products, on="product_id", how="left")
    df = pd.merge(df, df_sellers, on="seller_id", how="left")
    
    # Reviews
    reviews_unique = df_reviews.drop_duplicates(subset=['order_id'], keep='last')
    df = pd.merge(df, reviews_unique[['order_id', 'review_score']], on="order_id", how="left")
    
    # Pagamentos (Mantendo detalhes de parcelamento)
    payments_agg = df_payments.groupby('order_id').agg({
        'payment_value': 'sum',
        'payment_installments': 'max',
        'payment_type': lambda x: x.iloc[0] # Pega o tipo principal
    }).reset_index()
    df = pd.merge(df, payments_agg, on="order_id", how="left")

    # Feature Engineering
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Métricas de Tempo
    df['tempo_entrega_previsto'] = (df['order_estimated_delivery_date'] - df['order_approved_at']).dt.days
    df['tempo_entrega_real'] = (df['order_delivered_customer_date'] - df['order_approved_at']).dt.days
    df['dias_atraso'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
    df['flag_atraso'] = (df['dias_atraso'] > 0).astype(int)
    
    # Sazonalidade
    df['ano_mes'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    df['dia_semana'] = df['order_purchase_timestamp'].dt.day_name()
    df['hora_compra'] = df['order_purchase_timestamp'].dt.hour
    
    # Financeiro (Conforme notebook Samuel)
    df['receita_liquida'] = df['price'] + df['freight_value']
    
    return df
