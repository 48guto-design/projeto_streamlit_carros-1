import streamlit as st
import pandas as pd
import plotly.express as px

# ============================
# Carregar dados
# ============================
df = pd.read_csv("data/vehicles.csv")

# Remover o .0 dos anos
df["model_year"] = df["model_year"].astype("Int64")

# Traduzir tipos de veículos
df["type"] = df["type"].replace({
    "SUV": "SUV",
    "sedan": "Sedan",
    "pickup": "Pickup",
    "truck": "Camião",
    "wagon": "Carrinha",
    "mini-van": "Monovolume",
    "convertible": "Descapotável",
    "coupe": "Coupé",
    "hatchback": "Hatchback",
    "offroad": "Todo-o-terreno",
    "van": "Carrinha Comercial",
    "bus": "Autocarro"
})

# ============================
# Título
# ============================
st.title("📊 Dashboard Completo de Veículos")

st.markdown("""
Este dashboard apresenta uma análise exploratória do mercado de veículos usados,
permitindo visualizar tendências de preços, quilometragem, fabricantes e condições dos veículos.
""")

# ============================
# Filtros
# ============================
st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    "Ano do veículo",
    sorted(df["model_year"].dropna().unique())
)

tipos = st.sidebar.multiselect(
    "Tipo de veículo",
    sorted(df["type"].dropna().unique())
)

condicoes = st.sidebar.multiselect(
    "Condição",
    sorted(df["condition"].dropna().unique())
)

df_filtrado = df.copy()

if anos:
    df_filtrado = df_filtrado[df_filtrado["model_year"].isin(anos)]

if tipos:
    df_filtrado = df_filtrado[df_filtrado["type"].isin(tipos)]

if condicoes:
    df_filtrado = df_filtrado[df_filtrado["condition"].isin(condicoes)]

# ============================
# Métricas gerais
# ============================
st.subheader("📌 Métricas gerais")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Preço médio",
    f"${df_filtrado['price'].mean():,.2f}"
)

col2.metric(
    "Quilometragem média",
    f"{df_filtrado['odometer'].mean():,.0f} km"
)

col3.metric(
    "Total de veículos",
    f"{df_filtrado.shape[0]}"
)

# ============================
# Histograma de preços
# ============================
st.subheader("📊 Distribuição dos preços dos veículos")

fig_hist = px.histogram(
    df_filtrado,
    x="price",
    nbins=50,
    title="Distribuição dos preços dos veículos",
    labels={
        "price": "Preço do veículo (USD)",
        "count": "Quantidade de veículos"
    }
)

fig_hist.update_layout(
    xaxis_title="Preço do veículo (USD)",
    yaxis_title="Quantidade de veículos"
)

st.plotly_chart(fig_hist, use_container_width=True)

# ============================
# Gráfico de dispersão
# ============================
st.subheader("📈 Relação entre preço e quilometragem")

fig_disp = px.scatter(
    df_filtrado,
    x="odometer",
    y="price",
    color="type",
    hover_data=["model", "condition", "fuel"],
    title="Relação entre preço de venda e quilometragem",
    labels={
        "odometer": "Quilometragem (km)",
        "price": "Preço do veículo (USD)",
        "type": "Tipo de veículo"
    }
)

fig_disp.update_layout(
    xaxis_title="Quilometragem (km)",
    yaxis_title="Preço do veículo (USD)",
    legend_title="Tipo de veículo"
)

st.plotly_chart(fig_disp, use_container_width=True)

# ============================
# Fabricante x Tipo
# ============================
st.subheader("🚗 Distribuição dos tipos de veículos por modelo")

fig_fabricante = px.histogram(
    df_filtrado,
    x="model",
    color="type",
    title="Quantidade de veículos por modelo e categoria",
    labels={
        "model": "Modelo do veículo",
        "count": "Quantidade de veículos",
        "type": "Tipo de veículo"
    }
)

fig_fabricante.update_layout(
    xaxis_title="Modelo do veículo",
    yaxis_title="Quantidade de veículos",
    legend_title="Tipo de veículo",
    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_fabricante,
    use_container_width=True,
    key="grafico_modelos"
)

# ============================
# Condição x Ano
# ============================
st.subheader("📅 Distribuição dos anos dos veículos por condição")

fig_condicao = px.box(
    df_filtrado,
    x="condition",
    y="model_year",
    color="condition",
    title="Distribuição dos anos dos veículos por condição",
    labels={
        "condition": "Condição do veículo",
        "model_year": "Ano de fabrico"
    }
)

fig_condicao.update_layout(
    xaxis_title="Condição do veículo",
    yaxis_title="Ano de fabrico"
)

st.plotly_chart(fig_condicao, use_container_width=True)

# ============================
# Dados completos
# ============================
st.subheader("📋 Dados completos")

st.dataframe(df_filtrado)