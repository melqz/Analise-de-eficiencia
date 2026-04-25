# Análise de Eficiência Operacional em Entregas Logísticas

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo principal desenvolver um sistema de análise abrangente para monitorar a performance de entregas logísticas, identificar atrasos e gargalos operacionais, avaliar a eficiência geral e gerar insights acionáveis para a melhoria contínua dos processos. A abordagem simula um cenário real de negócios, utilizando ferramentas de análise de dados para extrair valor de informações operacionais.

## 🧱 Estrutura do Projeto e Metodologia

O projeto foi estruturado em fases distintas, cobrindo desde a criação da base de dados até a geração de insights e visualizações, conforme a metodologia a seguir:

### 1. Base de Dados Simulada

Para este projeto, foi criada uma base de dados simulada em formato Excel (`base_logistica.xlsx`), contendo as seguintes tabelas:

*   **Entregas:** Registros individuais de cada entrega, incluindo `id_entrega`, `data_envio`, `data_entrega`, `status` (entregue, atrasado, cancelado), `id_cliente`, `id_motorista`, `id_rota` e `valor_frete`.
*   **Motoristas:** Informações sobre os motoristas, como `id_motorista`, `nome` e `regiao`.
*   **Rotas:** Detalhes das rotas, incluindo `id_rota`, `cidade`, `estado` e `distancia_km`.
*   **Clientes:** Dados dos clientes, como `id_cliente`, `segmento` e `cidade`.

Foram gerados aproximadamente 1000 registros de entregas, com variações realistas de status e tempos de entrega para simular um ambiente operacional dinâmico.

### 2. Análise SQL (Extração e Análise Exploratória)

Utilizando Python com as bibliotecas Pandas e SQLite (em memória), foram executadas diversas queries para extrair e analisar os dados, simulando a etapa de ETL (Extract, Transform, Load) e a análise exploratória. As principais queries realizadas foram:

#### Taxa de Entrega por Status

```sql
SELECT 
  status,
  COUNT(*) AS total,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM entregas), 2) AS percentual
FROM entregas
GROUP BY status;
```

**Resultado:**

| status    | total | percentual |
|:----------|------:|-----------:|
| atrasado  |    54 |        5.4 |
| cancelado |    21 |        2.1 |
| entregue  |   925 |       92.5 |

#### Tempo Médio de Entrega

```sql
SELECT 
  AVG(julianday(data_entrega) - julianday(data_envio)) AS tempo_medio_dias
FROM entregas
WHERE status != 'cancelado';
```

**Resultado:**

| tempo_medio_dias |
|-----------------:|
|         3.127681 |

#### Top 5 Rotas com Mais Atrasos

```sql
SELECT 
  r.cidade,
  r.estado,
  COUNT(e.id_entrega) AS total_atrasos
FROM entregas e
JOIN rotas r ON e.id_rota = r.id_rota
WHERE e.status = 'atrasado'
GROUP BY r.id_rota
ORDER BY total_atrasos DESC
LIMIT 5;
```

**Resultado:**

| cidade         | estado | total_atrasos |
|:---------------|:-------|--------------:|
| Manaus         | AM     |            11 |
| Recife         | PE     |             7 |
| Salvador       | BA     |             6 |
| Porto Alegre   | RS     |             6 |
| Rio de Janeiro | RJ     |             6 |

#### Performance por Motorista (Taxa de Atraso)

```sql
SELECT 
  m.nome,
  COUNT(e.id_entrega) AS total_entregas,
  SUM(CASE WHEN e.status = 'atrasado' THEN 1 ELSE 0 END) AS total_atrasos,
  ROUND(SUM(CASE WHEN e.status = 'atrasado' THEN 1 ELSE 0 END) * 100.0 / COUNT(e.id_entrega), 2) AS taxa_atraso_percent
FROM entregas e
JOIN motoristas m ON e.id_motorista = m.id_motorista
GROUP BY m.id_motorista
ORDER BY taxa_atraso_percent DESC;
```

**Resultado:**

| nome         | total_entregas | total_atrasos | taxa_atraso_percent |
|:-------------|---------------:|--------------:|--------------------:|
| Motorista 5  |             65 |             7 |               10.77 |
| Motorista 3  |             58 |             6 |               10.34 |
| Motorista 14 |             62 |             6 |                9.68 |
| Motorista 1  |             66 |             6 |                9.09 |
| Motorista 6  |             70 |             5 |                7.14 |
| Motorista 12 |             70 |             4 |                5.71 |
| Motorista 15 |             69 |             3 |                4.35 |
| Motorista 4  |             70 |             3 |                4.29 |
| Motorista 13 |             73 |             3 |                4.11 |
| Motorista 8  |             73 |             3 |                4.11 |
| Motorista 7  |             66 |             2 |                3.03 |
| Motorista 2  |             66 |             2 |                3.03 |
| Motorista 10 |             73 |             2 |                2.74 |
| Motorista 9  |             59 |             1 |                1.69 |
| Motorista 11 |             60 |             1 |                1.67 |

### 3. Modelagem de Dados e Cálculo de Métricas (DAX-like)

A modelagem de dados foi concebida seguindo o padrão **Star Schema**, onde a tabela de `Entregas` atua como a **Tabela Fato**, e as tabelas `Motoristas`, `Rotas`, `Clientes` e uma dimensão de `Tempo` (criada a partir das datas de envio) funcionam como **Tabelas Dimensão**. Este modelo facilita a análise e a criação de métricas complexas.

As seguintes métricas, análogas às criadas em DAX no Power BI, foram calculadas em Python:

*   **Total de Entregas (não canceladas):** 979
*   **% No Prazo:** 94.48%
*   **Tempo Médio de Entrega:** 3.13 dias
*   **Ticket Médio de Frete:** R$ 280.35

### 4. Visualizações e Dashboards de Performance

Foram gerados gráficos para representar os principais indicadores de performance logística, simulando os dashboards de um sistema de BI. As visualizações incluem:

#### Dashboard 1: Visão Geral - Distribuição de Status das Entregas

![Distribuição de Status das Entregas](https://private-us-east-1.manuscdn.com/sessionFile/Dzum2MaissZVgXzraAJTty/sandbox/hsvu2yeWTkGUZbFs7gPGJ9-images_1777130619347_na1fn_L2hvbWUvdWJ1bnR1L2Rhc2hib2FyZF92aXNhb19nZXJhbA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvRHp1bTJNYWlzc1pWZ1h6cmFBSlR0eS9zYW5kYm94L2hzdnUyeWVXVGtHVVpiRnM3Z1BHSjktaW1hZ2VzXzE3NzcxMzA2MTkzNDdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyUmhjMmhpYjJGeVpGOTJhWE5oYjE5blpYSmhiQS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=FIFGYIrVhSALeROV4l9QvG6IRRdPZzFGQ5qSTfkSQ6F3Jk8cADV60s5g0-nT9BOD-5N-CdHFQ4~vGAb6UiqqkCXbHukFt~BTc7Z7TnF~Ut58RAYhJprcy9coZ7lfgw1QIYttlEMg0Z9AouUHEBi7TWModPfnDsYVy7SD1JAnO7Dxd5tzy2zoibnQ-IO75nkshQ4AwRjUEtwY7zd1-S~ULl9~lE90vZYuTBIawCeFnqCSZ-QVSzekQJlajVID7GOJJFiYc0uC4na3dD-N2pPAQ3BVnYVZ0shOk10IPBJ16qI4pB89Hps6H6T7SDalZ5PrM1R9p6FQGl7JJ1tvsXbyAQ__)

#### Dashboard 2: Operacional - Tempo Médio de Entrega por Cidade

![Tempo Médio de Entrega por Cidade](https://private-us-east-1.manuscdn.com/sessionFile/Dzum2MaissZVgXzraAJTty/sandbox/hsvu2yeWTkGUZbFs7gPGJ9-images_1777130619347_na1fn_L2hvbWUvdWJ1bnR1L2Rhc2hib2FyZF9vcGVyYWNpb25hbA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvRHp1bTJNYWlzc1pWZ1h6cmFBSlR0eS9zYW5kYm94L2hzdnUyeWVXVGtHVVpiRnM3Z1BHSjktaW1hZ2VzXzE3NzcxMzA2MTkzNDdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyUmhjMmhpYjJGeVpGOXZjR1Z5WVdOcGIyNWhiQS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=anrd33K7OnwMIIrqc~38zVtQ4OhEUHMs4m789yVOe4oOzuESIA75OYNxxjt4mNFvcDUq~KOmdznPiD1mHr-vD2fmPU7BbyatARWloRKRrjcMHfxdhuqbVBOCRY-5f1c653efvlQ0g3x-y0m0MDZYPHneRH9cQQp1EHgL7XdC7qg~j~VcMONeyzTcRBtNp982RbeV0IT1C5AztAOPVRZvG~Yd2LvdsHDyNvbW6eSsVEgcVhKaiXlDD0zITi7Dxh~YhA4uWUOvgQuvo5QRsJlfrfbKOm~OeJLypN5fptNCr5bu760shJmftj7FS7gEUyER0PWqqovBoJUAjTxyhGO2NQ__)

#### Dashboard 3: Performance - Taxa de Atraso por Motorista

![Taxa de Atraso por Motorista](https://private-us-east-1.manuscdn.com/sessionFile/Dzum2MaissZVgXzraAJTty/sandbox/hsvu2yeWTkGUZbFs7gPGJ9-images_1777130619347_na1fn_L2hvbWUvdWJ1bnR1L2Rhc2hib2FyZF9wZXJmb3JtYW5jZQ.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvRHp1bTJNYWlzc1pWZ1h6cmFBSlR0eS9zYW5kYm94L2hzdnUyeWVXVGtHVVpiRnM3Z1BHSjktaW1hZ2VzXzE3NzcxMzA2MTkzNDdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyUmhjMmhpYjJGeVpGOXdaWEptYjNKdFlXNWpaUS5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=u6Hmvympt6hQh1z3ApwTxKl3sSjjQCZ6NudRMwGUj8DzUebjm3CVDZlhX5iTcm37aTBVL4fUllkoZHN2VVOCm-czS55wVxrNSdYgH9k038muWc3QE0MKl~ifOblftephU7XFuxrAW4tARtMcSggM22yPnGUU3XJnN4Oa4Qbo4VWuidW3p8o6ih-zCeIAKKD1c~FdO07yt0aDyBUXI7zHacvHREgEaMASOtzuj3OPiCPKIlrcyiBK3Ku5euiGpR0H6PAB87pGu4x0pKa3x5kPI8CRXnqUBrw3B69qZuui9fjWDzTRp2qLbiOa0oEaI1DdGe-q-Fq9R5Tel1lYs34eCQ__)

#### Evolução Temporal do Volume de Entregas

![Evolução Mensal do Volume de Entregas](https://private-us-east-1.manuscdn.com/sessionFile/Dzum2MaissZVgXzraAJTty/sandbox/hsvu2yeWTkGUZbFs7gPGJ9-images_1777130619347_na1fn_L2hvbWUvdWJ1bnR1L2V2b2x1Y2FvX3RlbXBvcmFs.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvRHp1bTJNYWlzc1pWZ1h6cmFBSlR0eS9zYW5kYm94L2hzdnUyeWVXVGtHVVpiRnM3Z1BHSjktaW1hZ2VzXzE3NzcxMzA2MTkzNDdfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyVjJiMngxWTJGdlgzUmxiWEJ2Y21Gcy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=IrZgaWI5M6wHJpiaDH928iQOD3H0l5EbttzklWzLZmMGDO1oroWWPtKcozp5vWVuv0pQGfj1ROoZlOXQRk2v5aLl3Q9N5V958TuizCbke8ufYdWifSots8WCmzVXJbHwhC3l6SNGDLR-BtYXX91PkicBpnBVNsDO8JuPvpRKcMqmuJJDII9Vl2h0k53Qq3NLXfr~2JpTm0vrdWnf2s1tsigwErSqyFKmJh5xOGZNsazcdcxEkK9Nyju4-L9eVp6C6u~uHHWjApL6y3IbVDJNJOXg0ZHZF3e84S79KlqIL2i0TAfyELjFJl-lS8CtpnwNupRHGQGEX5VfiEPQTH2I6g__)

### 5. Insights Gerados

Com base na análise dos dados e nas visualizações, os seguintes insights podem ser extraídos:

*   **Alta Eficiência Geral:** A taxa de entregas no prazo de 94.48% indica uma operação logística geralmente eficiente, com uma pequena parcela de atrasos (5.4%) e cancelamentos (2.1%).
*   **Gargalos Regionais:** Cidades como Manaus, Recife e Porto Alegre apresentam os maiores tempos médios de entrega e/ou maior número de atrasos, sugerindo a necessidade de investigação sobre as condições de rota, infraestrutura local ou volume de entregas nessas regiões.
*   **Performance Individual de Motoristas:** Há uma variação significativa na performance dos motoristas. Motoristas como o 'Motorista 5' e 'Motorista 3' apresentam taxas de atraso consideravelmente mais altas que a média, indicando a necessidade de treinamento, otimização de rotas ou redistribuição de carga de trabalho para esses indivíduos.
*   **Oportunidades de Otimização de Rotas:** As rotas com maior distância (implicadas pelo tempo base de entrega) podem estar correlacionadas com os atrasos, especialmente em regiões mais remotas ou com infraestrutura desafiadora. Uma análise mais aprofundada das rotas específicas e suas características pode revelar oportunidades de otimização.
*   **Monitoramento Contínuo:** A evolução temporal do volume de entregas mostra a necessidade de um monitoramento contínuo para identificar picos e vales, permitindo um planejamento proativo da capacidade logística.

## 📦 Entrega Final (Portfólio)

Este documento serve como a entrega final do projeto, consolidando:

*   A explicação do problema e o objetivo.
*   A metodologia e as ferramentas utilizadas (Python, Pandas, SQLite, Matplotlib, Seaborn).
*   As queries SQL documentadas e seus resultados.
*   A modelagem de dados e as métricas calculadas.
*   As visualizações de dashboards geradas.
*   Os insights acionáveis para melhoria da eficiência logística.

Este projeto demonstra a capacidade de transformar dados brutos em informações estratégicas, utilizando uma abordagem completa de análise de dados para resolver problemas de negócios reais.
🎓 Competências Demonstradas

✅ Análise de Dados: SQL, Pandas, agregações complexas
✅ Modelagem: Star Schema, dimensões, fatos
✅ Visualização: Plotly, Matplotlib, Streamlit
✅ Python: Scripts completos, tratamento de dados
✅ Business Intelligence: KPIs, métricas, insights
✅ Comunicação: Documentação clara, insights acionáveis
✅ Pensamento Crítico: Identificação de problemas e soluções


