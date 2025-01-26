import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from mlxtend.frequent_patterns import apriori, association_rules

# movies.csv dosyasını oku
movies_df = pd.read_csv('archive/movie.csv')

# genres sütununu virgülle ayırarak liste haline getirme
movies_df['genres'] = movies_df['genres'].str.split('|')

# MultiLabelBinarizer ile kategorileri ikili değerlere dönüştürme
mlb = MultiLabelBinarizer()
genre_movie_matrix = mlb.fit_transform(movies_df['genres'])

# Matrisi True/False değerleriyle dönüştürme
genre_movie_matrix = genre_movie_matrix.astype(bool)  # 1'i True, 0'ı False'a dönüştürür

# Matrisi DataFrame'e dönüştürme
genre_movie_df = pd.DataFrame(genre_movie_matrix, columns=mlb.classes_)

# Sonuçları yazdır
print(genre_movie_df)

# Apriori algoritmasını çalıştır
frequent_itemsets = apriori(genre_movie_df, min_support=0.4, use_colnames=True)

# Apriori sonuçlarını yazdır
print(frequent_itemsets)

# İlişki kuralları oluşturma
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=1)

# İlişki kurallarını CSV dosyasına kaydetme
rules.to_csv("genre_association_rules.csv", index=False)

# Kuralları yazdır
print(rules)
