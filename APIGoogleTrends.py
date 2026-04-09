import pandas as pd
from pytrends.request import TrendReq
import os

print("Conectando ao Google Trends...")
# Configurando o idioma para PT-BR e o fuso horário
pytrends = TrendReq(hl='pt-BR', tz=180)

# Palavras-chave que fazem sentido para a nossa análise de estoque
palavras_chave = ["comprar online", "frete grátis", "perfume", "relogio"]

print(f"Buscando tendências para: {palavras_chave}")

# Construindo a requisição
pytrends.build_payload(kw_list=palavras_chave,
                       cat=0,
                       timeframe='2017-01-01 2018-08-31',
                       geo='BR')

# Puxando o interesse ao longo do tempo
df_trends = pytrends.interest_over_time()

# Removendo a coluna 'isPartial'
if 'isPartial' in df_trends.columns:
    df_trends = df_trends.drop(columns=['isPartial'])

print("\nColeta concluída!")

print(df_trends.head())

# Garantindo que a pasta existe antes de salvar
caminho_destino = './dados_olist'
if not os.path.exists(caminho_destino):
    os.makedirs(caminho_destino)

# Salvando no CSV
df_trends.to_csv(f'{caminho_destino}/tendencias_google.csv')
print("\nArquivo de tendências salvo com sucesso!")