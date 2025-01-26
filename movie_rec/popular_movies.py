import pandas as pd

# Dosyaları yükleme
movies = pd.read_csv("archive/movie.csv")
ratings = pd.read_csv("Updated_DataSet/filtered_rating_.csv")

# Dosyaları movieId üzerinden birleştirme
merged_data = pd.merge(ratings, movies, on="movieId", how="inner")

# Film türlerini manuel belirleme 
selected_genres = ["Adventure", "Comedy", "Drama", "Romance", "Fantasy", "Crime", "Sci-Fi", "Action", "Thriller", "Documentary"]

# Her tür için popüler filmleri bulma
popular_movies = pd.DataFrame(columns=["movieId", "title", "view_count", "avr_rating", "popularite_puani"])

for genre in selected_genres:
    # Belirli türdeki filmleri filtreleme
    genre_data = merged_data[merged_data["genres"].str.contains(genre, na=False)]
    
    # İzlenme sayısı ve ortalama rating'i hesaplama
    genre_grouped = genre_data.groupby(["movieId", "title"]).agg(
        view_count=("userId", "count"),
        avr_rating=("rating", "mean")
    ).reset_index()

    # Popülarite puanını hesaplama
    genre_grouped["popularite_puani"] = genre_grouped["view_count"] * genre_grouped["avr_rating"]
    
    # En popüler 50 filmi seçme
    top_50 = genre_grouped.nlargest(50, "popularite_puani")
    
    # Daha önce eklenmemiş filmleri kontrol et ve ekle
    popular_movies = pd.concat([popular_movies, top_50]).drop_duplicates(subset="movieId", keep="first")

# Popülarite puanına göre sıralama
popular_movies = popular_movies.sort_values(by="popularite_puani", ascending=False)

# CSV dosyasına kaydetme
popular_movies.to_csv("popular_movies.csv", index=False)

print("Popüler filmler 'popular_movies.csv' dosyasına kaydedildi.")
