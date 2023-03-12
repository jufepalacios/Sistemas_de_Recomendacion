import streamlit as st

st.set_page_config(
    page_title="App - Sistemas Recomendación",
    page_icon=":three:",
)

st.write("# Sistemas de Recomendación - Canciones :notes:")

st.sidebar.success("Selecciona una página de arriba.")

st.markdown(
    """
    En esta aplicación se exploraron un conjunto de datos obtenido de la red social
    de música *Last.fm*.

    De los datos, se entrenaron modelos de recomendación colaborativo para que la aplicación sea capaz de recomendarle canciones dados sus gustos musicales.

    Ingrese o Registrese ahora.
"""
)