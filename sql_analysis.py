import pandas as pd
import sqlite3

# Carregar dados do Excel
excel_file = '/home/ubuntu/base_logistica.xlsx'
df_entregas = pd.read_excel(excel_file, sheet_name='entregas')
df_motoristas = pd.read_excel(excel_file, sheet_name='motoristas')
df_rotas = pd.read_excel(excel_file, sheet_name='rotas')
df_clientes = pd.read_excel(excel_file, sheet_name='clientes')

# Criar conexão SQLite em memória
conn = sqlite3.connect(':memory:')

# Salvar DataFrames como tabelas SQL
df_entregas.to_sql('entregas', conn, index=False)
df_motoristas.to_sql('motoristas', conn, index=False)
df_rotas.to_sql('rotas', conn, index=False)
df_clientes.to_sql('clientes', conn, index=False)

def run_query(query, title):
    print(f"\n--- {title} ---")
    result = pd.read_sql_query(query, conn)
    print(result)
    return result

# Query 1: Taxa de entrega por status
query1 = """
SELECT 
  status,
  COUNT(*) AS total,
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM entregas), 2) AS percentual
FROM entregas
GROUP BY status;
"""
run_query(query1, "Taxa de Entrega por Status")

# Query 2: Tempo médio de entrega (excluindo cancelados)
query2 = """
SELECT 
  AVG(julianday(data_entrega) - julianday(data_envio)) AS tempo_medio_dias
FROM entregas
WHERE status != 'cancelado';
"""
run_query(query2, "Tempo Médio de Entrega")

# Query 3: Top 5 rotas com mais atrasos
query3 = """
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
"""
run_query(query3, "Top 5 Rotas com Mais Atrasos")

# Query 4: Performance por Motorista (Taxa de Atraso)
query4 = """
SELECT 
  m.nome,
  COUNT(e.id_entrega) AS total_entregas,
  SUM(CASE WHEN e.status = 'atrasado' THEN 1 ELSE 0 END) AS total_atrasos,
  ROUND(SUM(CASE WHEN e.status = 'atrasado' THEN 1 ELSE 0 END) * 100.0 / COUNT(e.id_entrega), 2) AS taxa_atraso_percent
FROM entregas e
JOIN motoristas m ON e.id_motorista = m.id_motorista
GROUP BY m.id_motorista
ORDER BY taxa_atraso_percent DESC;
"""
run_query(query4, "Performance por Motorista")

conn.close()
