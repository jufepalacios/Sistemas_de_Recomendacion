import streamlit as st

st.set_page_config(
    page_title="App - Grupo",
    page_icon=":three:",
)

st.write("# Taller 1 - Sistemas de Recomendación :notes:")

st.sidebar.success("Selecciona una página de arriba.")

st.markdown(
    """
    En este laboratorio se exploraron un conjuto de datos obtenido de una red social
    de música *Last.fm*.

    De estos datos se entrenaron modelos de recomendación colaborativo usuario - usuario e item - item.

    Los resultados se muestran en esta aplicación Web

    ### Objetivos
    - Desarrollar y evaluar un modelo colaborativo de recomendación de información
    - Realizar una práctica sobre un dataset real
"""
)