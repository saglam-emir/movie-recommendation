import pandas as pd

df_movie = pd.read_csv("archive/movie.csv")
df_rating = pd.read_csv("archive/rating.csv")

df_new_rating = pd.read_csv("Updated_DataSet/filtered_rating_.csv")

df_rules = pd.read_csv("association_rules.csv")

df_popular_movie = pd.read_csv("popular_movies.csv")
