import pandas as pd
from read_csv import df_new_rating
from mlxtend.preprocessing import TransactionEncoder

# Kullanıcıların izlediği filmleri liste haline getirme
data = df_new_rating.groupby("userId")["movieId"].apply(list).tolist()

# TransactionEncoder ile ikili (binary) matris oluşturma
te = TransactionEncoder()
te_data = te.fit(data).transform(data)

# True-False matrisi 1 ve 0'a çevirme
user_movie_matrix = pd.DataFrame(te_data, columns=te.columns_)

print(user_movie_matrix)
