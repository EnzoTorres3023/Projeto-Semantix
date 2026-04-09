import os
# Importando a biblioteca do Kaggle (lembre-se de ter o kaggle.json na pasta certa!)
import kaggle

# Definindo onde os arquivos vão ser salvos
caminho_destino = './dados_olist'

# Criando a pasta se ela não existir
if not os.path.exists(caminho_destino):
    os.makedirs(caminho_destino)

print("Iniciando o download do dataset da Olist...")

# Fazendo o download e já descompactando (unzip=True)
kaggle.api.dataset_download_files(
    'olistbr/brazilian-ecommerce',
    path=caminho_destino,
    unzip=True
)

print(f"Sucesso! Seus CSVs fresquinhos estão na pasta: {caminho_destino}")