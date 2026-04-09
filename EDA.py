import pandas as pd
import numpy as np
import os

# 1. Carregando os dados
caminho = "./dados_olist"

print("Carregando bases com Pandas")
df_orders = pd.read_csv(f"{caminho}/olist_orders_dataset.csv")
df_items = pd.read_csv(f"{caminho}/olist_order_items_dataset.csv")
df_products = pd.read_csv(f"{caminho}/olist_products_dataset.csv")
df_reviews = pd.read_csv(f"{caminho}/olist_order_reviews_dataset.csv")
df_customers = pd.read_csv(f"{caminho}/olist_customers_dataset.csv")

# 2. Limpeza e Pré-processamento
print("Limpando e processando dados")

# Tratamento de Nulos nos Reviews
df_reviews['review_comment_message'] = df_reviews['review_comment_message'].fillna("Sem comentário")

# Padronização de Datas
date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    df_orders[col] = pd.to_datetime(df_orders[col])

# Calculando o tempo de entrega em dias
df_orders['tempo_entrega_dias'] = (df_orders['order_delivered_customer_date'] - df_orders['order_purchase_timestamp']).dt.days

# Removendo Outliers e pedidos não entregues
df_orders_clean = df_orders[(df_orders['order_status'] == 'delivered') & (df_orders['tempo_entrega_dias'] > 0)].copy()
df_items_clean = df_items[df_items['price'] <= 3000].copy()

# 3. Cruzamento de Dados (Merge)
df_completo = df_items_clean.merge(df_orders_clean, on="order_id") \
                            .merge(df_products, on="product_id") \
                            .merge(df_reviews, on="order_id") \
                            .merge(df_customers, on="customer_id")

# Simulando o SQL
print("\nEstatísticas por Categoria")
stats_cat = df_completo.groupby('product_category_name').agg(
    volume_vendas=('order_item_id', 'count'),
    preco_medio=('price', 'mean'),
    preco_mediano=('price', 'median'),
    dispersao_preco=('price', 'std')
).sort_values(by='volume_vendas', ascending=False).head(10)
print(stats_cat)

print("\nPrazo de Entrega por Estado")
entrega_estado = df_completo.groupby('customer_state')['tempo_entrega_dias'].mean().sort_values(ascending=False).head(5)
print(entrega_estado)

# IDENTIFICAÇÃO DE VARIÁVEIS E CORRELAÇÕES
print("\nCorrelação: Tempo de Entrega vs Nota do Cliente")
correlacao = df_completo['tempo_entrega_dias'].corr(df_completo['review_score'])
print(f"Coeficiente de Correlação: {correlacao:.4f}")
if correlacao < 0:
    print("Conclusão: Correlação negativa! Quanto maior o tempo de entrega, menor a nota do cliente. Ruptura logística destrói reputação.")

# ANÁLISE DE SAZONALIDADE
print("\nSazonalidade: Vendas de Beleza/Saúde por Mês")
df_completo['mes_compra'] = df_completo['order_purchase_timestamp'].dt.month
sazonalidade = df_completo[df_completo['product_category_name'] == 'beleza_saude'].groupby('mes_compra')['order_id'].count()
print(sazonalidade)

print("\nEDA concluída!")

# --- PREPARANDO DADOS PARA O LOOKER STUDIO ---
print("Gerando base para o Dashboard")

# Agrupando por categoria com as métricas cruciais
df_looker = df_completo.groupby('product_category_name').agg(
    volume_vendas=('order_item_id', 'count'),
    faturamento_total=('price', 'sum'),
    nota_media=('review_score', 'mean')
).reset_index()

# Calculando Ticket Médio
df_looker['ticket_medio'] = df_looker['faturamento_total'] / df_looker['volume_vendas']

# Criando a Curva ABC baseada no faturamento
df_looker = df_looker.sort_values(by='faturamento_total', ascending=False)
df_looker['perc_faturamento'] = df_looker['faturamento_total'] / df_looker['faturamento_total'].sum()
df_looker['perc_acumulado'] = df_looker['perc_faturamento'].cumsum()

# Função para classificar A (70%), B (20%) e C (10%)
def classifica_abc(perc):
    if perc <= 0.70: return 'A (Curva Vital)'
    elif perc <= 0.90: return 'B (Intermediários)'
    else: return 'C (Cauda Longa)'

df_looker['classificacao_abc'] = df_looker['perc_acumulado'].apply(classifica_abc)

# Salvando o arquivo final
df_looker.to_csv('./dados_olist/base_looker_studio.csv', index=False)
print("Arquivo 'base_looker_studio.csv' pronto")