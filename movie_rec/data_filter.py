import pandas as pd

# rating.csv dosyasını yükle
ratings = pd.read_csv("rating.csv")

# Gereksiz sütunu sil
ratings = ratings.drop(columns=["timestamp"])

# Kullanıcı başına izlenen film sayısını hesapla
user_counts = ratings["userId"].value_counts()

# 100'den az film izleyen kullanıcıları filtrele
filtered_ratings = ratings[ratings["userId"].isin(user_counts[user_counts >= 100].index)]

# Sonuçları filtered_rating_.csv dosyasına kaydet
filtered_ratings.to_csv("filtered_rating_.csv", index=False)

print("Filtrelenmiş veriler 'filtered_rating_.csv' dosyasına kaydedildi.")
