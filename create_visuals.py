import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Carregar dados
df = pd.read_csv('/home/ubuntu/fato_logistica.csv')
df['data_envio'] = pd.to_datetime(df['data_envio'])

# 1. Dashboard 1: Visão Geral - Status das Entregas
plt.figure(figsize=(10, 6))
status_counts = df['status'].value_counts()
colors = ['#2ecc71', '#e74c3c', '#95a5a6']
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Distribuição de Status das Entregas', fontsize=15)
plt.savefig('/home/ubuntu/dashboard_visao_geral.png')
plt.close()

# 2. Dashboard 2: Operacional - Tempo Médio por Rota (Top 10)
plt.figure(figsize=(12, 6))
rota_performance = df[df['status'] != 'cancelado'].groupby('cidade')['tempo_entrega_dias'].mean().sort_values(ascending=False)
sns.barplot(x=rota_performance.values, y=rota_performance.index, palette='viridis')
plt.title('Tempo Médio de Entrega por Cidade (Dias)', fontsize=15)
plt.xlabel('Dias')
plt.ylabel('Cidade')
plt.savefig('/home/ubuntu/dashboard_operacional.png')
plt.close()

# 3. Dashboard 3: Performance - Ranking de Motoristas (Taxa de Atraso)
plt.figure(figsize=(12, 6))
motorista_atraso = df.groupby('nome').apply(lambda x: (x['status'] == 'atrasado').mean() * 100).sort_values(ascending=False)
sns.barplot(x=motorista_atraso.values, y=motorista_atraso.index, palette='magma')
plt.title('Taxa de Atraso por Motorista (%)', fontsize=15)
plt.xlabel('Percentual de Atraso')
plt.ylabel('Motorista')
plt.savefig('/home/ubuntu/dashboard_performance.png')
plt.close()

# 4. Evolução Temporal de Entregas
plt.figure(figsize=(12, 6))
df['mes_envio'] = df['data_envio'].dt.to_period('M')
evolucao = df.groupby('mes_envio').size()
evolucao.plot(kind='line', marker='o', color='#3498db', linewidth=2)
plt.title('Evolução Mensal do Volume de Entregas', fontsize=15)
plt.xlabel('Mês')
plt.ylabel('Total de Entregas')
plt.savefig('/home/ubuntu/evolucao_temporal.png')
plt.close()

print("Visualizações geradas com sucesso.")
