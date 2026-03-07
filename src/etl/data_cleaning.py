import pandas as pd
import numpy as np
import os
import argparse
import warnings

warnings.filterwarnings("ignore")


def load_and_filter_orders(raw_dir):
    """Carrega os pedidos e aplica filtros iniciais de status e conversão de datas.

    Args:
        raw_dir (str): Diretório contendo o arquivo olist_orders_dataset.csv.

    Returns:
        pd.DataFrame: DataFrame de pedidos filtrado e com datas convertidas.
    """
    path_orders = os.path.join(raw_dir, "olist_orders_dataset.csv")
    cols_orders = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    orders = pd.read_csv(path_orders, usecols=cols_orders)

    # Filtro de Status: Manter apenas pedidos válidos para análise (agora APENAS entregues)
    valid_status = ["delivered"]
    orders = orders[orders["order_status"].isin(valid_status)].copy()

    # Tratamento Temporal
    dt_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in dt_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    return orders


def map_regiao(estado):
    """Mapeia a sigla de um estado brasileiro para sua respectiva macro-região.

    Args:
        estado (str): Sigla do estado (ex: 'SP', 'AM').

    Returns:
        str: Nome da região ou 'Desconhecido'.
    """
    regioes = {
        "Norte": ["AM", "RR", "AP", "PA", "TO", "RO", "AC"],
        "Nordeste": ["MA", "PI", "CE", "RN", "PE", "PB", "SE", "AL", "BA"],
        "Centro-Oeste": ["MT", "MS", "GO", "DF"],
        "Sudeste": ["SP", "RJ", "ES", "MG"],
        "Sul": ["PR", "RS", "SC"],
    }
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return "Desconhecido"

def feature_engineering(df):
    """Realiza a engenharia de variáveis para logística e regionalidade.

    Args:
        df (pd.DataFrame): DataFrame consolidado com dados de pedidos, clientes e vendedores.

    Returns:
        pd.DataFrame: DataFrame com as novas colunas calculadas.
    """
    # 1. SLA Real (Tempo de Espera em Dias)
    # Calculado apenas para pedidos onde a data de entrega existe
    df["tempo_espera_dias"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 3600)

    # 2. Atraso de entrega
    df["dias_atraso"] = (
        df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
    ).dt.total_seconds() / (24 * 3600)
    df["entregue_no_prazo"] = np.where(df["dias_atraso"] <= 0, 1, 0)

    # 3. Agrupamentos Geográficos (Regiões)
    if "customer_state" in df.columns:
        df["customer_regiao"] = df["customer_state"].apply(map_regiao)
    if "seller_state" in df.columns:
        df["seller_regiao"] = df["seller_state"].apply(map_regiao)

    # 4. Rotas Logísticas
    if "customer_state" in df.columns and "seller_state" in df.columns:
        df["rota_logistica"] = df["seller_state"] + " -> " + df["customer_state"]
        df["tipo_rota"] = np.where(
            df["seller_regiao"] == df["customer_regiao"],
            "Intra-regional",
            "Inter-regional",
        )

    return df


def treat_outliers_iqr(df, column):
    """Aplica o método IQR para remover outliers de uma coluna específica.

    Args:
        df (pd.DataFrame): DataFrame a ser tratado.
        column (str): Nome da coluna para remoção de outliers.

    Returns:
        pd.DataFrame: DataFrame limpo sem os outliers da coluna especificada.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    outliers_count = outliers_mask.sum()
    print(
        f"[{column}] Limites IQR: {lower_bound:.2f} a {upper_bound:.2f} | Outliers removidos: {outliers_count}"
    )

    return df[~outliers_mask].copy()


def build_cleaned_dataset(raw_dir, out_path):
    """Executa o pipeline completo de limpeza e preparação de dados.

    Lê os dados brutos, realiza merges, aplica engenharia de variáveis,
    trata outliers e exporta o dataset final.

    Args:
        raw_dir (str): Diretório raiz dos arquivos CSV brutos.
        out_path (str): Caminho para salvar o CSV processado.

    Returns:
        None: O resultado é salvo em disco.
    """
    print("1. Carregando e limpando Orders...")
    orders = load_and_filter_orders(raw_dir)

    print("2. Carregando tabelas complementares (filtrando colunas inúteis)...")
    cols_items = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "price",
        "freight_value",
    ]
    items = pd.read_csv(
        os.path.join(raw_dir, "olist_order_items_dataset.csv"), usecols=cols_items
    )

    # Removendo tamanho do nome e dimensões, mas MANTENDO metadados de descrição do produto
    cols_products = [
        "product_id",
        "product_category_name",
        "product_description_lenght",
    ]
    products = pd.read_csv(
        os.path.join(raw_dir, "olist_products_dataset.csv"), usecols=cols_products
    )

    cols_customers = ["customer_id", "customer_city", "customer_state"]
    customers = pd.read_csv(
        os.path.join(raw_dir, "olist_customers_dataset.csv"), usecols=cols_customers
    )

    cols_sellers = ["seller_id", "seller_city", "seller_state"]
    sellers = pd.read_csv(
        os.path.join(raw_dir, "olist_sellers_dataset.csv"), usecols=cols_sellers
    )

    cols_payments = [
        "order_id",
        "payment_type",
        "payment_installments",
        "payment_value",
    ]
    payments = pd.read_csv(
        os.path.join(raw_dir, "olist_order_payments_dataset.csv"), usecols=cols_payments
    )

    print(
        "3. Carregando e agregando Reviews (para manter descrições/comentários dos pedidos)..."
    )
    cols_reviews = ["order_id", "review_score", "review_comment_message"]
    reviews = pd.read_csv(
        os.path.join(raw_dir, "olist_order_reviews_dataset.csv"), usecols=cols_reviews
    )
    # Agregando por pedido (caso haja mais de um review, pegamos o último/mais recente)
    reviews_agg = (
        reviews.groupby("order_id")
        .agg({"review_score": "mean", "review_comment_message": "last"})
        .reset_index()
    )

    print("4. Realizando Joins (Merges)...")
    # Base no grão de itens (um pedido pode ter múltiplos itens/produtos)
    df = orders.merge(items, on="order_id", how="inner")
    df = df.merge(products, on="product_id", how="left")
    df = df.merge(customers, on="customer_id", how="left")
    df = df.merge(sellers, on="seller_id", how="left")
    df = df.merge(reviews_agg, on="order_id", how="left")

    # Tratamento Típico de Pagamentos (Olist_Order_Payments)
    # Filtro de parcelas: focar de 1 a 12 (excluindo anomalias de 24x sem sentido)
    valid_installments = payments[payments["payment_installments"].between(1, 12)]

    # Como um pedido pode ter pago com múltiplos cartões, agrupamos o pagamento por pedido
    pay_agg = (
        valid_installments.groupby("order_id")
        .agg(
            {
                "payment_value": "sum",
                "payment_installments": "max",
                "payment_type": lambda x: (
                    x.mode()[0] if not x.mode().empty else "unknown"
                ),
            }
        )
        .reset_index()
    )

    df = df.merge(pay_agg, on="order_id", how="left")

    print(f"Dimensão após Joins: {df.shape}")

    print("5. Feature Engineering (SLA, Regiões, Rotas)...")
    df = feature_engineering(df)

    print("6. Tratamento de Outliers (Regras Exploratórias)...")

    # 5.1 Outliers Logísticos (Cap temporal em 100 dias, remover SLA negativo irracional)
    sla_mask = df["tempo_espera_dias"].notnull() & (
        (df["tempo_espera_dias"] < 0) | (df["tempo_espera_dias"] > 100)
    )
    print(
        f"[tempo_espera] Removendo outliers extremos de entrega (Negativo ou >100 dias): {sla_mask.sum()}"
    )
    df = df[~sla_mask].copy()

    # 5.2 Outliers Monetários/Frete (IQR) - Para evitar viés em ML e painéis corporativos
    df = treat_outliers_iqr(df, "price")
    df = treat_outliers_iqr(df, "freight_value")
    # df = treat_outliers_iqr(df, 'payment_value') # Menos crítico, focamos no item

    print(f"Dimensão Final após tratamento completo: {df.shape}")

    print(f"7. Exportando Dataset Limpo para: {out_path} ...")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print("🚀 Pipeline de Limpeza concluído com sucesso!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script para Limpeza e Preparação de Dados da Olist"
    )

    # Valores default genéricos baseados na raiz do projeto
    default_raw = os.path.join("data", "raw")
    default_out = os.path.join("data", "processed", "olist_cleaned_dataset.csv")

    parser.add_argument(
        "--raw", default=default_raw, help="Pasta contendo os arquivos originais .csv"
    )
    parser.add_argument(
        "--out", default=default_out, help="Caminho do arquivo de saída limpo"
    )

    args = parser.parse_args()
    build_cleaned_dataset(args.raw, args.out)