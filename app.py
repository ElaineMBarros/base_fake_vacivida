import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar base de dados
@st.cache_data
def load_data():
    return pd.read_csv("vacivida_base_unificada.csv", low_memory=False)

df = load_data()

st.title("📊 Análise Interativa - Base Vacivida")

st.markdown("Explore estatísticas descritivas, correlações e distribuições de dados anonimizados sobre eventos adversos pós-vacinação.")

# ----------------- FILTROS ------------------
st.sidebar.header("🔎 Filtros")

# Idade
if 'VCVD_IDADE' in df.columns:
    min_idade = int(df['VCVD_IDADE'].min())
    max_idade = int(df['VCVD_IDADE'].max())
    idade_range = st.sidebar.slider("Idade", min_value=min_idade, max_value=max_idade, value=(min_idade, max_idade))
    df = df[df['VCVD_IDADE'].between(*idade_range)]

# Sexo
if 'VCVD_SEXO' in df.columns:
    sexos = df['VCVD_SEXO'].dropna().unique().tolist()
    sexo_select = st.sidebar.multiselect("Sexo", sexos, default=sexos)
    df = df[df['VCVD_SEXO'].isin(sexo_select)]

# UF do atendimento
if 'VCVD_UF_ATENDIMENTO_MEDICO' in df.columns:
    ufs = df['VCVD_UF_ATENDIMENTO_MEDICO'].dropna().unique().tolist()
    uf_select = st.sidebar.multiselect("UF Atendimento Médico", ufs, default=ufs)
    df = df[df['VCVD_UF_ATENDIMENTO_MEDICO'].isin(uf_select)]

# Ano da Notificação
if 'VCVD_DATA_NOTIFICACAO' in df.columns:
    df['VCVD_DATA_NOTIFICACAO'] = pd.to_datetime(df['VCVD_DATA_NOTIFICACAO'], errors='coerce')
    anos = df['VCVD_DATA_NOTIFICACAO'].dt.year.dropna().unique()
    if len(anos) > 0:
        ano_range = st.sidebar.slider("Ano da Notificação", int(anos.min()), int(anos.max()), (int(anos.min()), int(anos.max())))
        df = df[df['VCVD_DATA_NOTIFICACAO'].dt.year.between(*ano_range)]

# ----------------- ANÁLISES ------------------
st.subheader("📈 Estatísticas Descritivas")
colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
col_select = st.multiselect("Selecione variáveis numéricas:", colunas_numericas, default=colunas_numericas[:5])

if col_select:
    st.dataframe(df[col_select].describe().T)

    # Boxplots com correção no eixo Y
    st.subheader("📦 Boxplot das Variáveis Selecionadas")
    for col in col_select:
        dados_box = df[col].dropna()
        if dados_box.nunique() > 1:
            fig, ax = plt.subplots()
            sns.boxplot(y=dados_box, ax=ax)
            ax.set_title(f"Boxplot - {col}")
            st.pyplot(fig)
        else:
            st.info(f"A variável '{col}' não tem dados suficientes para um boxplot.")

# Correlação
st.subheader("🔗 Correlação entre Variáveis")
if len(col_select) >= 2:
    corr = df[col_select].corr()
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.info("Selecione pelo menos duas variáveis para ver a correlação.")

# Histograma
st.subheader("📊 Distribuição de Variável Numérica")
col_hist = st.selectbox("Escolha uma variável para o histograma:", colunas_numericas)
if col_hist:
    fig, ax = plt.subplots()
    df[col_hist].dropna().hist(bins=20, ax=ax)
    ax.set_title(f"Distribuição de {col_hist}")
    st.pyplot(fig)