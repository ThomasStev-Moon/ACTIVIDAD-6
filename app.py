import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Coink Analytics", layout="wide")
st.title("🏦 Coink – Análisis de Usuarios OINK")

@st.cache_data
def cargar():
    return pd.read_csv("usuarios_calificados.csv")

df = cargar()

col1, col2, col3 = st.columns(3)
col1.metric("Usuarios totales", len(df))
col2.metric("Score promedio", f"{df['coink_score'].mean():.1f}")
col3.metric("Monto total", f"${df['monto_total'].sum():,.0f}")

st.subheader("Distribución de categorías")
st.bar_chart(df['categoria'].value_counts())

st.subheader("Top 20 usuarios")
st.dataframe(df.nlargest(20, 'coink_score'))

st.subheader("Frecuencia vs Monto")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='num_depositos', y='monto_total',
                hue='categoria', ax=ax)
ax.set_yscale('log')
st.pyplot(fig)

uid = st.selectbox("Selecciona un usuario", df['user_id'])
st.write(df[df['user_id']==uid])