import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações iniciais
np.random.seed(42)
random.seed(42)
num_entregas = 1000

# 1. Tabela de Motoristas
motoristas_data = {
    'id_motorista': range(1, 16),
    'nome': [f'Motorista {i}' for i in range(1, 16)],
    'regiao': random.choices(['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'], k=15)
}
df_motoristas = pd.DataFrame(motoristas_data)

# 2. Tabela de Rotas
rotas_data = {
    'id_rota': range(1, 11),
    'cidade': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador', 'Recife', 'Fortaleza', 'Brasília', 'Manaus'],
    'estado': ['SP', 'RJ', 'MG', 'PR', 'RS', 'BA', 'PE', 'CE', 'DF', 'AM'],
    'distancia_km': [random.randint(50, 1000) for _ in range(10)]
}
df_rotas = pd.DataFrame(rotas_data)

# 3. Tabela de Clientes
clientes_data = {
    'id_cliente': range(1, 51),
    'segmento': random.choices(['Varejo', 'Indústria', 'E-commerce'], k=50),
    'cidade': random.choices(df_rotas['cidade'].tolist(), k=50)
}
df_clientes = pd.DataFrame(clientes_data)

# 4. Tabela de Entregas
data_inicio = datetime(2024, 1, 1)
entregas = []

for i in range(1, num_entregas + 1):
    id_motorista = random.choice(df_motoristas['id_motorista'].tolist())
    id_rota = random.choice(df_rotas['id_rota'].tolist())
    id_cliente = random.choice(df_clientes['id_cliente'].tolist())
    
    data_envio = data_inicio + timedelta(days=random.randint(0, 90))
    
    # Lógica de entrega: 
    # Distância influencia o tempo base
    dist = df_rotas.loc[df_rotas['id_rota'] == id_rota, 'distancia_km'].values[0]
    tempo_base = max(1, dist // 200)
    
    # Adicionar aleatoriedade e atrasos
    atraso_aleatorio = random.choices([0, 1, 2, 5], weights=[70, 15, 10, 5])[0]
    tempo_total = tempo_base + atraso_aleatorio
    
    data_entrega = data_envio + timedelta(days=int(tempo_total))
    
    # Status baseado em um SLA fixo de 4 dias para simplificar ou dinâmico
    sla = 4 if dist < 500 else 7
    is_atrasado = (data_entrega - data_envio).days > sla
    
    status = 'atrasado' if is_atrasado else 'entregue'
    # Pequena chance de cancelado
    if random.random() < 0.02:
        status = 'cancelado'
        data_entrega = np.nan

    entregas.append({
        'id_entrega': i,
        'data_envio': data_envio,
        'data_entrega': data_entrega,
        'status': status,
        'id_cliente': id_cliente,
        'id_motorista': id_motorista,
        'id_rota': id_rota,
        'valor_frete': round(random.uniform(50, 500), 2)
    })

df_entregas = pd.DataFrame(entregas)

# Salvar em Excel com múltiplas abas
with pd.ExcelWriter('/home/ubuntu/base_logistica.xlsx') as writer:
    df_entregas.to_excel(writer, sheet_name='entregas', index=False)
    df_motoristas.to_excel(writer, sheet_name='motoristas', index=False)
    df_rotas.to_excel(writer, sheet_name='rotas', index=False)
    df_clientes.to_excel(writer, sheet_name='clientes', index=False)

print("Base de dados gerada com sucesso: /home/ubuntu/base_logistica.xlsx")
