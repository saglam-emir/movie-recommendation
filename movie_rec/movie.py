# HERBİR KATEGORİ İÇİN EN POPÜLER 50 FİLM BU ŞEKİLDE BULUNUYOR

import pandas as pd

# # Dosyaları yükleme
movies = pd.read_csv("archive/movie.csv")
ratings = pd.read_csv("Updated_DataSet/filtered_rating_.csv")

# # Dosyaları movieId üzerinden birleştirme
merged_data = pd.merge(ratings, movies, on="movieId", how="inner")



# #Film türlerini manuel belirleme 
selected_genres = ["Adventure","Comedy","Drama","Romance","Fantasy","Crime","Sci-Fi","Action","Thriller","Documentary"]

# # Her tür için filtreleme ve popüler filmleri bulma
popular_movies = {}

for genre in selected_genres:
     # Belirli türdeki filmleri filtreleme
     genre_data = merged_data[merged_data["genres"].str.contains(genre, na=False)]
    
#     # İzlenme sayısı ve ortalama rating'i hesaplama
     genre_grouped = genre_data.groupby(["movieId","title"]).agg(
         izlenme_sayisi=("userId", "count"),
         ortalama_rating=("rating", "mean")
          
     ).reset_index()

     # Popularite puanını hesaplama
     genre_grouped["popularite_puani"] = genre_grouped["izlenme_sayisi"] * genre_grouped["ortalama_rating"]
    
    
#     # En popüler 50 filmi seçme
     popular_movies[genre] = genre_grouped.nlargest(50, "popularite_puani").reset_index(drop=True)
     

# # Örnek: Aksiyon türünde en popüler filmleri görüntüleme
print("Crime Türünde En Popüler Filmler:")
print(popular_movies["Crime"][["movieId", "title", "izlenme_sayisi", "ortalama_rating","popularite_puani"]])

