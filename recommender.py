import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 

df_ratings=pd.read_csv("ratings.csv")
df_movies=pd.read_csv("movies.csv")
df_genres=df_movies['genres'].str.get_dummies(sep='|')

df_movies=pd.merge(df_movies, df_genres, left_index=True, right_index=True)
df_movies.drop(['genres'], axis = 1,inplace=True)

df_movies['year']=df_movies['title']
df_movies['title'] = [x[:-7] for x in df_movies['title']]
df_movies['year'] = [x[-5:-1] for x in df_movies['year']]

final_dataset = df_ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.fillna(0,inplace=True)

no_user_voted = df_ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = df_ratings.groupby('userId')['rating'].agg('count')

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > no_user_voted.min()].index,:]
final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > no_movies_voted.median()].index]

from scipy.sparse import csr_matrix
csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)
final_dataset.head()

from sklearn.neighbors import NearestNeighbors
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_jobs=-1)
knn.fit(csr_data)

def get_movie_recommendation(movie_name):
    n_movies_to_reccomend = 10
    movie_list = df_movies[df_movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = df_movies[df_movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':df_movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df['Title'].tolist()
    else:
        return "No movies found. Please check your input"
    
# movie=input()

# print("Recommendation for movie :  {}\n".format(movie))
# recommended_movies = get_movie_recommendation(movie)
# print(recommended_movies)