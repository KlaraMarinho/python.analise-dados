import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Dashboard Interativo - Canais de Data Science no YouTube")
st.sidebar.header("Filtros")

@st.cache_data
def carregar_dados():
    df = pd.read_csv("dataset/data_science_youtube.csv")
    
    # Limpeza de dados:
    # - Remoção de duplicados
    df.drop_duplicates(inplace=True)
    
    # - Tratamento de valores ausentes
    df.fillna({
        "Views": 0,
        "Like_count": 0,
        "Comment_Count": 0
    }, inplace=True)

    df["Published_date"] = pd.to_datetime(df["Published_date"], errors='coerce')

    # - Remoção de linhas com datas inválidas ou inconsistências
    df = df.dropna(subset=["Published_date"])

    return df

df = carregar_dados()

df['Month_Year'] = df['Published_date'].dt.to_period("M")

st.subheader("Visão Geral dos Dados")
st.write(df.describe())
st.write("Exemplo de Dados:")
st.write(df.head())

# Filtros para análise interativa
canal_selecionado = st.sidebar.multiselect(
    "Selecione os canais:",
    options=df["Channel_Name"].unique(),
    default=df["Channel_Name"].unique()
)

dados_filtrados = df[df["Channel_Name"].isin(canal_selecionado)]

st.subheader("Estatísticas Gerais")
st.write(f"Total de vídeos: {len(dados_filtrados)}")
st.write(f"Visualizações totais: {dados_filtrados['Views'].sum():,.0f}")
st.write(f"Likes totais: {dados_filtrados['Like_count'].sum():,.0f}")
st.write(f"Comentários totais: {dados_filtrados['Comment_Count'].sum():,.0f}")

# Gráfico 1: Visualizações totais por canal
st.subheader("Visualizações Totais por Canal")
vis_canal = dados_filtrados.groupby("Channel_Name")["Views"].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots()
vis_canal.plot(kind="bar", ax=ax1, color="skyblue")
ax1.set_ylabel("Total de Visualizações")
st.pyplot(fig1)

# Gráfico 2: Engajamento ao longo do tempo
st.subheader("Engajamento ao Longo do Tempo")
engajamento_tempo = dados_filtrados.groupby("Month_Year")[["Views", "Like_count", "Comment_Count"]].sum()
fig2 = px.line(
    engajamento_tempo,
    x=engajamento_tempo.index.astype(str),
    y=["Views", "Like_count", "Comment_Count"],
    labels={"value": "Engajamento", "Month_Year": "Mês/Ano"},
    title="Engajamento ao Longo do Tempo"
)
st.plotly_chart(fig2)

# Gráfico 3: Distribuição de visualizações
st.subheader("Distribuição de Visualizações (Boxplot)")
fig3 = px.box(
    dados_filtrados,
    x="Channel_Name",
    y="Views",
    title="Distribuição de Visualizações por Canal",
    labels={"Views": "Visualizações", "Channel_Name": "Canal"}
)
st.plotly_chart(fig3)

# Exportação de dados filtrados
st.sidebar.download_button(
    label="Baixar Dados Filtrados",
    data=dados_filtrados.to_csv(index=False),
    file_name="dados_filtrados.csv",
    mime="text/csv"
)
