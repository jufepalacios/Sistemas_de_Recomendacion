import streamlit as st
import sqlite3 

conn = sqlite3.connect('data.db')
cur = conn.cursor()

def login_user(username,password):
	cur.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username,password))
	data = cur.fetchall()
	return data

st.set_page_config(page_title="Log In")

placeholder = st.empty()
placeholder_side = st.sidebar.empty()

placeholder.markdown("""
# Log In

Por favor diligencie su usuario y contraseña en el menu de la izquierda.
""")

side_container = placeholder_side.container()
side_container.header("Log In")
username = side_container.text_input("Usuario :")
password = side_container.text_input("Contraseña :",type='password')
login_button = side_container.button('Log In')

if login_button:
    if login_user(username,password):
        side_container.empty()
        placeholder_side.button('Log Out')
        placeholder.markdown("# Bienvenido Usuario {}".format(username))

    else:
       side_container.warning("Usuario o Contraseña incorrectos")


