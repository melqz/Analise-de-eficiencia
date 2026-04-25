import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Logístico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar dados
@st.cache_data
def load_data():
    excel_file = '/home/ubuntu/base_logistica.xlsx'
    df_entregas = pd.read_excel(excel_file, sheet_name='entregas')
    df_motoristas = pd.read_excel(excel_file, sheet_name='motoristas')
    df_rotas = pd.read_excel(excel_file, sheet_name='rotas')
    df_clientes = pd.read_excel(excel_file, sheet_name='clientes')
    
    # Converter datas
    df_entregas['data_envio'] = pd.to_datetime(df_entregas['data_envio'])
    df_entregas['data_entrega'] = pd.to_datetime(df_entregas['data_entrega'])
    
    # Calcular tempo de entrega
    df_entregas['tempo_entrega_dias'] = (df_entregas['data_entrega'] - df_entregas['data_envio']).dt.days
    
    # Merge com dimensões
    df_fato = df_entregas.merge(df_motoristas, on='id_motorista', how='left')
    df_fato = df_fato.merge(df_rotas, on='id_rota', how='left')
    df_fato = df_fato.merge(df_clientes, on='id_cliente', how='left', suffixes=('', '_cliente'))
    
    return df_fato, df_entregas, df_motoristas, df_rotas, df_clientes

df_fato, df_entregas, df_motoristas, df_rotas, df_clientes = load_data()

# Título principal
st.markdown("# 📊 Dashboard de Performance Logística")
st.markdown("---")

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Filtro de Status
status_filter = st.sidebar.multiselect(
    "Status da Entrega",
    options=df_fato['status'].unique(),
    default=df_fato['status'].unique()
)

# Filtro de Cidade
cidade_filter = st.sidebar.multiselect(
    "Cidade de Destino",
    options=df_fato['cidade'].unique(),
    default=df_fato['cidade'].unique()
)

# Filtro de Segmento
segmento_filter = st.sidebar.multiselect(
    "Segmento de Cliente",
    options=df_fato['segmento'].unique(),
    default=df_fato['segmento'].unique()
)

# Aplicar filtros
df_filtrado = df_fato[
    (df_fato['status'].isin(status_filter)) &
    (df_fato['cidade'].isin(cidade_filter)) &
    (df_fato['segmento'].isin(segmento_filter))
]

# KPIs Principais
st.markdown("## 📈 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

total_entregas = len(df_filtrado[df_filtrado['status'] != 'cancelado'])
entregas_no_prazo = len(df_filtrado[df_filtrado['status'] == 'entregue'])
percent_no_prazo = (entregas_no_prazo / total_entregas * 100) if total_entregas > 0 else 0
tempo_medio = df_filtrado[df_filtrado['status'] != 'cancelado']['tempo_entrega_dias'].mean()
ticket_medio = df_filtrado['valor_frete'].mean()

with col1:
    st.metric("Total de Entregas", f"{total_entregas:,}", delta=None)

with col2:
    st.metric("% No Prazo", f"{percent_no_prazo:.1f}%", delta=None)

with col3:
    st.metric("Tempo Médio (dias)", f"{tempo_medio:.2f}", delta=None)

with col4:
    st.metric("Ticket Médio (R$)", f"{ticket_medio:.2f}", delta=None)

st.markdown("---")

# Abas para organizar dashboards
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🚛 Operacional", "👥 Performance", "📈 Análise Temporal"])

# TAB 1: Visão Geral
with tab1:
    st.markdown("### Distribuição de Status das Entregas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Pizza - Status
        status_counts = df_filtrado['status'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Status das Entregas",
            color_discrete_map={
                'entregue': '#2ecc71',
                'atrasado': '#e74c3c',
                'cancelado': '#95a5a6'
            },
            hole=0.3
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Gráfico de Pizza - Segmento
        segmento_counts = df_filtrado['segmento'].value_counts()
        fig_segmento = px.pie(
            values=segmento_counts.values,
            names=segmento_counts.index,
            title="Entregas por Segmento de Cliente",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.3
        )
        st.plotly_chart(fig_segmento, use_container_width=True)
    
    # Distribuição de Valor de Frete
    st.markdown("### Distribuição de Valor de Frete")
    fig_frete = px.histogram(
        df_filtrado,
        x='valor_frete',
        nbins=30,
        title="Histograma de Valores de Frete",
        color_discrete_sequence=['#3498db']
    )
    st.plotly_chart(fig_frete, use_container_width=True)

# TAB 2: Operacional
with tab2:
    st.markdown("### Análise Operacional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tempo médio por cidade
        st.markdown("#### Tempo Médio de Entrega por Cidade")
        tempo_por_cidade = df_filtrado[df_filtrado['status'] != 'cancelado'].groupby('cidade')['tempo_entrega_dias'].mean().sort_values(ascending=False)
        fig_tempo_cidade = px.bar(
            x=tempo_por_cidade.values,
            y=tempo_por_cidade.index,
            orientation='h',
            title="Tempo Médio por Cidade (dias)",
            color=tempo_por_cidade.values,
            color_continuous_scale='Viridis'
        )
        fig_tempo_cidade.update_layout(height=500)
        st.plotly_chart(fig_tempo_cidade, use_container_width=True)
    
    with col2:
        # Entregas por região
        st.markdown("#### Entregas por Região")
        regiao_counts = df_filtrado['regiao'].value_counts()
        fig_regiao = px.bar(
            x=regiao_counts.index,
            y=regiao_counts.values,
            title="Volume de Entregas por Região",
            labels={'x': 'Região', 'y': 'Total de Entregas'},
            color=regiao_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    # Tabela de Rotas com mais atrasos
    st.markdown("#### Top 10 Rotas com Mais Atrasos")
    rotas_atraso = df_filtrado[df_filtrado['status'] == 'atrasado'].groupby('cidade').size().sort_values(ascending=False).head(10)
    
    fig_rotas_atraso = px.bar(
        x=rotas_atraso.values,
        y=rotas_atraso.index,
        orientation='h',
        title="Rotas com Mais Atrasos",
        labels={'x': 'Total de Atrasos', 'y': 'Cidade'},
        color=rotas_atraso.values,
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_rotas_atraso, use_container_width=True)

# TAB 3: Performance
with tab3:
    st.markdown("### Performance de Motoristas")
    
    # Calcular performance por motorista
    motorista_performance = df_filtrado.groupby('nome').agg({
        'id_entrega': 'count',
        'status': lambda x: (x == 'atrasado').sum(),
        'tempo_entrega_dias': 'mean',
        'valor_frete': 'sum'
    }).rename(columns={
        'id_entrega': 'Total Entregas',
        'status': 'Total Atrasos',
        'tempo_entrega_dias': 'Tempo Médio (dias)',
        'valor_frete': 'Frete Total (R$)'
    })
    
    motorista_performance['Taxa Atraso (%)'] = (motorista_performance['Total Atrasos'] / motorista_performance['Total Entregas'] * 100).round(2)
    motorista_performance = motorista_performance.sort_values('Taxa Atraso (%)', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Taxa de Atraso
        st.markdown("#### Taxa de Atraso por Motorista")
        fig_motorista_atraso = px.bar(
            x=motorista_performance['Taxa Atraso (%)'].values,
            y=motorista_performance.index,
            orientation='h',
            title="Taxa de Atraso (%)",
            color=motorista_performance['Taxa Atraso (%)'].values,
            color_continuous_scale='RdYlGn_r'
        )
        fig_motorista_atraso.update_layout(height=600)
        st.plotly_chart(fig_motorista_atraso, use_container_width=True)
    
    with col2:
        # Gráfico de Tempo Médio
        st.markdown("#### Tempo Médio de Entrega por Motorista")
        fig_motorista_tempo = px.bar(
            x=motorista_performance['Tempo Médio (dias)'].values,
            y=motorista_performance.index,
            orientation='h',
            title="Tempo Médio (dias)",
            color=motorista_performance['Tempo Médio (dias)'].values,
            color_continuous_scale='Blues'
        )
        fig_motorista_tempo.update_layout(height=600)
        st.plotly_chart(fig_motorista_tempo, use_container_width=True)
    
    # Tabela detalhada de motoristas
    st.markdown("#### Tabela Detalhada de Performance")
    st.dataframe(motorista_performance, use_container_width=True)

# TAB 4: Análise Temporal
with tab4:
    st.markdown("### Análise Temporal")
    
    # Evolução mensal
    df_filtrado['mes_envio'] = df_filtrado['data_envio'].dt.to_period('M')
    evolucao_mensal = df_filtrado.groupby('mes_envio').size()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Evolução Mensal de Entregas")
        fig_evolucao = px.line(
            x=evolucao_mensal.index.astype(str),
            y=evolucao_mensal.values,
            title="Volume de Entregas por Mês",
            markers=True,
            labels={'x': 'Mês', 'y': 'Total de Entregas'}
        )
        fig_evolucao.update_traces(line=dict(color='#3498db', width=3))
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with col2:
        st.markdown("#### Status por Mês")
        status_mensal = df_filtrado.groupby(['mes_envio', 'status']).size().unstack(fill_value=0)
        fig_status_mensal = px.bar(
            x=status_mensal.index.astype(str),
            y=status_mensal.columns,
            title="Distribuição de Status por Mês",
            labels={'x': 'Mês', 'value': 'Total'},
            color_discrete_map={
                'entregue': '#2ecc71',
                'atrasado': '#e74c3c',
                'cancelado': '#95a5a6'
            }
        )
        st.plotly_chart(fig_status_mensal, use_container_width=True)
    
    # Heatmap de Atrasos por Dia da Semana e Hora
    st.markdown("#### Análise por Dia da Semana")
    df_filtrado['dia_semana'] = df_filtrado['data_envio'].dt.day_name()
    atraso_dia_semana = df_filtrado[df_filtrado['status'] == 'atrasado'].groupby('dia_semana').size()
    
    # Ordenar dias da semana
    dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_pt = {'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}
    
    atraso_dia_semana = atraso_dia_semana.reindex([d for d in dias_ordem if d in atraso_dia_semana.index])
    
    fig_dia_semana = px.bar(
        x=[dias_pt.get(d, d) for d in atraso_dia_semana.index],
        y=atraso_dia_semana.values,
        title="Atrasos por Dia da Semana",
        labels={'x': 'Dia da Semana', 'y': 'Total de Atrasos'},
        color=atraso_dia_semana.values,
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_dia_semana, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown("**Dashboard de Performance Logística** | Desenvolvido com Streamlit e Plotly | Dados Simulados para Análise")
