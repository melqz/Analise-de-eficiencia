import pandas as pd
import numpy as np

# Carregar dados
excel_file = '/home/ubuntu/base_logistica.xlsx'
df_entregas = pd.read_excel(excel_file, sheet_name='entregas')
df_motoristas = pd.read_excel(excel_file, sheet_name='motoristas')
df_rotas = pd.read_excel(excel_file, sheet_name='rotas')
df_clientes = pd.read_excel(excel_file, sheet_name='clientes')

# 1. Modelagem Star Schema (Conceitual no Python)
# Fato: df_entregas
# Dimensões: df_motoristas, df_rotas, df_clientes, df_calendario

# Criar Dimensão Calendário
df_entregas['data_envio'] = pd.to_datetime(df_entregas['data_envio'])
df_entregas['data_entrega'] = pd.to_datetime(df_entregas['data_entrega'])

min_date = df_entregas['data_envio'].min()
max_date = df_entregas['data_envio'].max()
df_calendario = pd.DataFrame({'data': pd.date_range(min_date, max_date)})
df_calendario['ano'] = df_calendario['data'].dt.year
df_calendario['mes'] = df_calendario['data'].dt.month
df_calendario['dia_semana'] = df_calendario['data'].dt.day_name()

# 2. Cálculos de Métricas (Equivalente ao DAX)

# Tempo de Entrega Real
df_entregas['tempo_entrega_dias'] = (df_entregas['data_entrega'] - df_entregas['data_envio']).dt.days

# % Entregas no Prazo (OTIF - On Time)
total_entregas = len(df_entregas[df_entregas['status'] != 'cancelado'])
entregas_no_prazo = len(df_entregas[df_entregas['status'] == 'entregue'])
percent_no_prazo = (entregas_no_prazo / total_entregas) * 100

# Tempo Médio de Entrega
tempo_medio = df_entregas[df_entregas['status'] != 'cancelado']['tempo_entrega_dias'].mean()

# Ticket Médio de Frete
ticket_medio_frete = df_entregas['valor_frete'].mean()

# 3. Enriquecimento da Fato para Visualização
df_fato = df_entregas.merge(df_motoristas, on='id_motorista', how='left')
df_fato = df_fato.merge(df_rotas, on='id_rota', how='left')
df_fato = df_fato.merge(df_clientes, on='id_cliente', how='left', suffixes=('', '_cliente'))

# Salvar Fato Enriquecida para a fase de Dashboard
df_fato.to_csv('/home/ubuntu/fato_logistica.csv', index=False)

print(f"Métricas Calculadas:")
print(f"- Total de Entregas (não canceladas): {total_entregas}")
print(f"- % No Prazo: {percent_no_prazo:.2f}%")
print(f"- Tempo Médio: {tempo_medio:.2f} dias")
print(f"- Ticket Médio Frete: R$ {ticket_medio_frete:.2f}")
print("\nArquivo 'fato_logistica.csv' gerado para visualização.")
