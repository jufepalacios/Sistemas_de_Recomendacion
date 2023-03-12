import streamlit as st
import sqlite3 
from datetime import date
import pandas as pd
import predictions as p

conn = sqlite3.connect('data.db')
cur = conn.cursor()

today = date.today()

def add_new(data):
	user = data[0]
	regi = data[1]
	pswd = data[2]
	gend = data[3]
	age = data[4]
	ctry = data[5]

	cur.execute('INSERT INTO users(user_id,gender,age,country,registered,password) VALUES ("{}","{}","{}","{}","{}","{}")'.format(user,gend,age,ctry,regi,pswd))
	conn.commit()

def add_preferences(username,data):
	for row in data:
		trac_id = get_track_id(row[:-1])
		play = row[-1]
		
		cur.execute('INSERT INTO preferences(user_id,track_id,playcount) VALUES ("{}","{}","{}")'.format(username,trac_id,play))
		conn.commit()

def get_track_id(data):
	artist = data[0]
	song = data[1]
	cur.execute('SELECT track_id FROM songs WHERE LOWER(artist_name) = LOWER("{}") AND LOWER(track_name) = LOWER("{}")'.format(artist,song))
	data = cur.fetchall()
	return data[0][0]

def get_all_preferences():
	cur.execute('SELECT * FROM preferences')
	data = cur.fetchall()
	df_preferences = pd.DataFrame(data, columns=['user_id','track_id','playcount'])
	return df_preferences
	
def convert_df(df):
	return df.to_csv().encode('utf-8')

st.set_page_config(page_title="Sign In")

placeholder = st.empty()
placeholder_side = st.sidebar.empty()
container_side = placeholder_side.container()

placeholder.markdown("""
# Sign In

En el menú de la izquierda, por favor diligencie el formulario para guardarlo en la base de datos.

Debe ingresar:

1. Usuario.
2. Contraseña.
3. Género.
4. Edad.
5. País.
6. Un archivo *.csv* con 3 columnas y la siguiente información:
	1. Nombre del artista.
	2. Nombre de la canción.
	3. Número de Reproducciones.
""")

username = container_side.text_input("Usuario")
password = container_side.text_input("Contraseña",type='password')
gender = container_side.selectbox("Género",('-','Femenino','Masculino'))
age = container_side.text_input("Edad")
country = container_side.selectbox("País",('-','Colombia'))
regis = today
uploaded_file = container_side.file_uploader("Escoja el archivo con sus preferencias")

new_user_list = []

signin_button = container_side.button('Sign In')

if signin_button:

	if username != '':
		new_user_list.append(username)
	else:
		container_side.warning('No ingresó un usuario')
		new_user_list = []

	new_user_list.append(regis)

	if password != '':
		new_user_list.append(password)
	else:
		container_side.warning('No ingresó una clave')
		new_user_list = []
	
	if gender != '-':
		if gender == 'Masculino':
			new_user_list.append('M')
		else:
			new_user_list.append('F')
		
	else:
		container_side.warning('No seleccionó un género')
		new_user_list = []

	if age.isnumeric() and int(age) < 100:
		new_user_list.append(age)
	else:
		container_side.warning('Edad invalida')
		new_user_list = []

	if country != '-':
		new_user_list.append(country)
	else:
		container_side.warning('Escoja un país')
		new_user_list = []

	if uploaded_file is not None:
		new_preferences = pd.read_csv(uploaded_file)
		new_preferences_list = new_preferences.values.tolist()
		new_user_list.append(new_preferences_list)
	else:
		container_side.warning('No ingresó un archivo con sus preferencias')
		new_user_list = []

	if len(new_user_list) == 7:
		add_new(new_user_list)
		add_preferences(new_user_list[0],new_user_list[-1])

		placeholder_side.empty()
		placeholder.empty()

		placeholder_side.button('Ingresar un nuevo usuario')

		df_new_user = pd.DataFrame([new_user_list[:-1]], columns=['Usuario','Fecha Registro','Contraseñaa','Genero','Edad','País'])
		df_vis = df_new_user[['Usuario','Genero','Edad','País','Fecha Registro']]
		
		df_preferences = get_all_preferences()
		p.train_model(df_preferences)

		st.markdown("# :bust_in_silhouette: Bienvenido, {}".format(username))
		st.markdown("Información del nuevo usuario:")
		st.table(df_vis)
		st.markdown("Preferencias del nuevo usuario:")
		st.dataframe(new_preferences)
		st.markdown(" ## Ya estás registrado! Ahora puedes ingresar a la aplicación")