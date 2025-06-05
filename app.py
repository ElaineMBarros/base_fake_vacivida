
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar a base
df = pd.read_csv("base_vacivida_anonimizada.csv")

st.title("📊 Dashboard Vacivida - Eventos Adversos Pós-Vacinação")

st.sidebar.header("Filtros")

# Filtros
sexo = st.sidebar.multiselect("Sexo", options=df['Sexo'].dropna().unique(), default=df['Sexo'].dropna().unique())
faixa_etaria = st.sidebar.multiselect("Faixa Etária", options=df['Faixa Etária'].dropna().unique(), default=df['Faixa Etária'].dropna().unique())
gestante = st.sidebar.multiselect("Gestante", options=df['Gestante'].dropna().unique(), default=df['Gestante'].dropna().unique())

# Aplicar filtros
df_filtered = df[
    (df['Sexo'].isin(sexo)) &
    (df['Faixa Etária'].isin(faixa_etaria)) &
    (df['Gestante'].isin(gestante))
]

st.subheader("Resumo dos Eventos Filtrados")
st.write(f"Total de registros: {len(df_filtered)}")

# Função para plotar gráficos
def plot_bar(coluna, titulo):
    fig, ax = plt.subplots()
    df_filtered[coluna].value_counts(dropna=False).plot(kind='bar', ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel(coluna)
    ax.set_ylabel("Número de Eventos")
    st.pyplot(fig)

# Gráficos
plot_bar("Sexo", "Distribuição por Sexo")
plot_bar("Faixa Etária", "Distribuição por Faixa Etária")
plot_bar("Evolução", "Evolução dos Casos")
plot_bar("Classificação Final", "Classificação Final dos Casos")
plot_bar("Gestante", "Eventos em Gestantes")
plot_bar("Raça/Cor", "Distribuição por Raça/Cor")
