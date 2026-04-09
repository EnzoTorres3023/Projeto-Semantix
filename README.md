# Projeto Semantrix: O Dilema do Estoque 📦
**O Custo Invisível do Excesso e da Falta no E-commerce Brasileiro**

Este projeto é a entrega final do curso de Análise de Dados da EBAC em parceria com a Semantrix. O objetivo é utilizar dados para solucionar as dores do gerenciamento de estoque em e-commerces, equilibrando o excesso (capital empatado) e a ruptura (perda de vendas e reputação).

📊 **[CLIQUE NO LINK AO LADO PARA ACESSAR O DASHBOARD INTERATIVO NO LOOKER STUDIO]** *(https://lookerstudio.google.com/reporting/dc4b7bef-6064-4ce7-b679-fa42c132f3ee)*

---

## 1. Coleta de Dados
Para modelar as soluções, utilizamos bases de dados públicas focadas no varejo brasileiro:
* **Olist E-commerce Dataset:** Dados estruturados e não estruturados de mais de 100 mil pedidos (2016-2018), extraídos via **API do Kaggle** diretamente no script Python.
* **Google Trends:** Séries temporais de interesse de busca, coletadas através da biblioteca `pytrends`, para avaliar sazonalidades macro do mercado.

## 2. Modelagem e Preparação dos Dados (EDA)
Todo o processamento foi realizado em **Python (Pandas)**. As principais etapas de modelagem incluíram:
* **Limpeza e Tratamento:** Preenchimento de nulos em textos de avaliações e padronização de formatos de data (timestamps).
* **Engenharia de Recursos (Feature Engineering):** Criação da variável `tempo_entrega_dias` (diferença entre a compra e a entrega real).
* **Estruturação Curva ABC:** Modelagem de um DataFrame consolidado agregando volume de vendas e faturamento para classificar os produtos dinamicamente em categorias A, B e C.

## 3. Conclusões e Insights
A Análise Exploratória e o Dashboard revelaram três pilares acionáveis para o negócio:

1. **O Efeito Pareto (Curva ABC):** As categorias *cama_mesa_banho*, *beleza_saude* e *esporte_lazer* dominam o faturamento. A ação proposta é a criação de uma blindagem de orçamento e estoques de segurança rigorosos para esses itens da Curva A.
2. **O Custo da Insatisfação (Logística Reversa):** Identificamos uma correlação negativa entre tempo de entrega e nota do cliente. Produtos "Ralo de Dinheiro" (alto volume, baixa avaliação por atrasos) devem sofrer bloqueio imediato de recompra para estancar perdas de margem.
3. **Previsibilidade Sazonal:** Constatamos que picos de demanda (ex: em *beleza_saude* entre Maio e Agosto) são seguidos por quedas abruptas. A recomendação é sincronizar ordens de compra ao modelo preditivo, evitando estocar no final da sazonalidade alta.
