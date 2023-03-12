from surprise.dump import dump, load
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
import pandas as pd

def save_model(algo):
  dump(file_name='user_user_model', algo=algo)

def train_model(ratings_df):
  reader = Reader(rating_scale=(1, ratings_df['playcount'].max()))
  train_set = Dataset.load_from_df(ratings_df[['user_id', 'track_id', 'playcount']], reader).build_full_trainset()
  algo_user = KNNBasic(sim_options={'name': 'pearson','user_based': True})
  algo_user.fit(train_set)
  save_model(algo_user)

def get_user_predictions(user_id, songs_list, size_predictions):
  algo = load('user_user_model')[1]
  test_set = [(user_id, song, 0) for song in songs_list]
  predictions=algo.test(test_set)

  user_predictions=list(filter(lambda x: x[0]==user_id,predictions))
  #Ordenamos de mayor a menor estimación de relevancia
  user_predictions.sort(key=lambda x : x.est, reverse=True)
  #tomamos las 10 primeras predicciones
  user_predictions=user_predictions[0:size_predictions]
  #Se convierte a dataframe
  df_predictions = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est) , user_predictions)))
  #Lo unimos con el dataframe de películas
  return df_predictions

def get_nearest_neighbor_list(user_id):
  algo = load('user_user_model')[1]
  nn_list = algo.get_neighbors(algo.trainset.to_inner_uid(user_id), k=MAX_NEIGHBORS_SHOW)
  nn_users_id = []
  for neighbor in nn_list:
    nn_users_id.append(algo.trainset.to_raw_uid(neighbor))
  return nn_users_id

MAX_NEIGHBORS_SHOW = 3
