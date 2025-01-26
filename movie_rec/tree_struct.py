import pandas as pd
from read_csv import df_rules
from read_csv import df_movie  # movie.csv verisinin okunduğu dosya

class TrieNode:
    def __init__(self):
        self.children = {}
        self.items = []

class TrieStruct:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, antecedents, consequents, support, confidence):
        node = self.root
        for char in antecedents:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.items.append((consequents, support, confidence))


def insertNode(tree):
    for index, row in df_rules.iterrows():
        antecedent = eval(row['antecedents'])
        consequent = eval(row['consequents'])
        support = row['support']
        confidence = row['confidence']
        tree.insert(antecedent, consequent, support, confidence)

def searchNode(tree, antecedents):
    node = tree.root
    for char in antecedents:
        if char not in node.children:
            return []
        node = node.children[char]
    return node.items


# Genre kontrol fonksiyonu
def check_movie_genre(movie_id, genre):
    movie_row = df_movie[df_movie['movieId'] == movie_id]
    if not movie_row.empty:
        genres = movie_row.iloc[0]['genres'].split('|')
        return genre in genres
    return False

# Ana öneri fonksiyonu
def recommend_high_confidence_movie(tree, user_films, genre):
    max_confidence = 0
    recommended_movie = None

    for film in user_films:
        # Kullanıcının izlediği her film için kuralları al
        rules = searchNode(tree, frozenset({film}))
        for consequents, support, confidence in rules:
            for item in consequents:
                # Filmin kategoriye uyup uymadığını kontrol et
                genre_ok = check_movie_genre(item, genre)
                if genre_ok:
                    if confidence > max_confidence:
                        max_confidence = confidence
                        recommended_movie = item
    
    return recommended_movie if recommended_movie else None

# Örnek kullanım
tree = TrieStruct()
insertNode(tree)
# user_films = [1, 1210, 32]  # Kullanıcının izlediği film ID'leri
# all_movies = df_movie['movieId'].tolist()
# desired_genre = "Action"  # Kullanıcının öneri istediği kategori

# recommended_movie_id = recommend_high_confidence_movie(tree, all_movies, desired_genre)
# if recommended_movie_id:
#     print(f"Önerilen film ID'si: {recommended_movie_id}")
# else:
#     print("Belirtilen kategoriye ait öneri bulunamadı.")