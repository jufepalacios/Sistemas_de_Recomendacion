import streamlit as st
import sqlite3 
import pandas as pd
import predictions as p

conn = sqlite3.connect('data.db')
cur = conn.cursor()

def login_user(username,password):
	cur.execute("SELECT * FROM users WHERE user_id = '{}' AND password = '{}'".format(username,password))
	data = cur.fetchall()
	return data

def data_user(username):
    cur.execute("SELECT user_id, gender, age, country, registered FROM users WHERE user_id = '{}'".format(username))
    data = cur.fetchall()
    return data

def most_liked_songs(username):
    cur.execute("SELECT s.artist_name, s.track_name, p.playcount FROM preferences p INNER JOIN songs s ON p.track_id = s.track_id AND artist_name != '' WHERE user_id = '{}' LIMIT 10".format(username))
    data = cur.fetchall()
    return data

def most_liked_artists(username):
    cur.execute("SELECT s.artist_name, COUNT(s.track_name), SUM(p.playcount) FROM preferences p INNER JOIN songs s ON p.track_id = s.track_id WHERE user_id = '{}' AND artist_name != '' GROUP BY 1 ORDER BY 3 DESC LIMIT 3".format(username))
    data = cur.fetchall()
    return data

def songs_not_listened(username):
    cur.execute("SELECT track_id FROM songs WHERE artist_name != '' AND track_id NOT IN (SELECT track_id FROM preferences WHERE user_id = '{}')".format(username))
    data = cur.fetchall()
    return data

def get_artist_song(df):
    list_track_id = df.values.tolist()
    list_songs = []
    for track in list_track_id:
        cur.execute("SELECT artist_name, track_name FROM songs WHERE track_id = '{}'".format(track[0]))
        data = cur.fetchall()[0]
        list_songs.append(data)
    return list_songs

def get_nn_artist_songs(list_usuarios):
    df = pd.DataFrame(columns=['Usuario','Género','Edad','País','Artista','Canción','Número de Reproducciones'])
    for usuario in list_usuarios:
        data_canciones = most_liked_songs(usuario)
        data_usuario = data_user(usuario)
        df_usuario = pd.DataFrame(data_usuario, columns=['Usuario','Género','Edad','País','Fecha Registro'])
        df_canciones = pd.DataFrame(data_canciones, columns=['Artista','Canción','Número de Reproducciones'])
        df_canciones['usuario'] = usuario
        df_u_c = df_usuario.merge(df_canciones,right_on='usuario',left_on='Usuario')[['Usuario','Género','Edad','País','Artista','Canción','Número de Reproducciones'   ]]
        df = pd.concat([df, df_u_c.iloc[:3]], ignore_index=True)
    return df

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

        placeholder_side.button('Log Out')
        placeholder.empty()
        st.markdown("# Hola de nuevo, {}".format(username))

        usuario = data_user(username)
        canciones = most_liked_songs(username)
        artistas = most_liked_artists(username)
        canciones_no = songs_not_listened(username)
        list_canciones_no = [item for t in canciones_no for item in t]

        df_usuario= pd.DataFrame(usuario, columns=['Usuario','Género','Edad','País','Fecha Registro'])
        df_canciones = pd.DataFrame(canciones, columns=['Artista','Canción','Número de Reproducciones'])
        df_artistas = pd.DataFrame(artistas, columns=['Artista','Total Canciones','Total Reproducciones'])

        recomendaciones = p.get_user_predictions(username,list_canciones_no,10)
        canciones_recomendadas = get_artist_song(recomendaciones)
        df_canciones_reco = pd.DataFrame(canciones_recomendadas, columns=['Artista','Canción'])

        usuarios_vecinos = p.get_nearest_neighbor_list(username)
        df_usuarios_vecinos_canciones = get_nn_artist_songs(usuarios_vecinos)

        st.markdown("### :bust_in_silhouette: Tus datos")
        st.dataframe(df_usuario)

        col1, col2 = st.columns(2)
        col1.markdown("### :musical_note: Tus canciones favoritas ")
        col1.dataframe(df_canciones)

        col2.markdown("### :crown: Tus artistas favoritos ")
        col2.dataframe(df_artistas)

        st.markdown("## :gift: Nuestra recomendación para ti")

        st.markdown("### Dado estos usuarios y sus gustos musicales")
        st.dataframe(df_usuarios_vecinos_canciones)

        st.markdown("### Te recomendamos las siguientes canciones")
        st.dataframe(df_canciones_reco)

    else:
       side_container.warning("Usuario o Contraseña incorrectos")