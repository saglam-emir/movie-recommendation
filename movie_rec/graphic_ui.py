import tkinter as tk
from tkinter import ttk, Listbox, messagebox
import pandas as pd
from read_csv import df_new_rating
from read_csv import df_movie 
from read_csv import df_popular_movie

from tree_struct import TrieNode, TrieStruct, insertNode, searchNode, recommend_high_confidence_movie

# Load datasets
# movie_df = pd.DataFrame({
#     'movieId': [1, 2, 3, 4, 5],
#     'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D', 'Movie E'],
#     'genres': ['Action', 'Comedy', 'Drama', 'Horror', 'Thriller']
# })

# filtered_rating_df = pd.DataFrame({
#     'userId': [101, 102, 103, 101, 102],
#     'movieId': [1, 2, 3, 4, 5],
#     'rating': [5, 4, 3, 5, 4],
#     'timestamp': [20240101, 20240102, 20240103, 20240104, 20240105]
# })

class MovieRecommendationApp:
    def __init__(self, root):
        
        # Ağacı başlatma 
        self.trie = TrieStruct()
        insertNode(self.trie)
        
        self.root = root
        self.root.title("Film Öneri Sistemi")
        self.root.geometry("600x500")
        
        # Initial Selections
        self.recommendation_type = tk.StringVar()
        self.search_type = tk.StringVar()
        self.user_listbox = None
        self.movie_listbox = None
        self.genre_listbox = None

        # Popular vs. Personalized Choice
        ttk.Label(root, text="İlk Seçim: Öneri Türü").pack(pady=5)
        ttk.Radiobutton(root, text="Popüler Film Önerileri", variable=self.recommendation_type, value="popular", command=self.toggle_user_listbox).pack()
        ttk.Radiobutton(root, text="Kişiselleştirilmiş Film Önerileri", variable=self.recommendation_type, value="personalized", command=self.toggle_user_listbox).pack()

        # User ID Listbox
        self.user_listbox = Listbox(root, height=5, state="normal")
        self.user_listbox.pack(pady=5)
        self.load_user_ids()

        # Second Selection Area
        ttk.Label(root, text="İkinci Seçim: Arama Türü").pack(pady=5)
        ttk.Radiobutton(root, text="Film Türüne Göre Öneriler", variable=self.search_type, value="genre", command=self.show_genre_listbox).pack()
        ttk.Radiobutton(root, text="Film İsmine Göre Öneriler", variable=self.search_type, value="title", command=self.show_movie_listbox).pack()

        # Genre Listbox
        self.genre_listbox = Listbox(root, height=5)
        self.genres =  ["Adventure","Comedy","Drama","Romance","Fantasy","Crime","Sci-Fi","Action","Thriller","Documentary"]
        for genre in self.genres:
            self.genre_listbox.insert(tk.END, genre)
        self.genre_listbox.pack(pady=5)
        self.genre_listbox.pack_forget()

        # Movie ID Listbox
        self.movie_listbox = Listbox(root, height=5)
        self.movie_listbox.pack(pady=5)
        self.movie_listbox.pack_forget()

        # Recommend Button
        self.recommend_button = ttk.Button(root, text="Öner", command=self.recommend_movie)
        self.recommend_button.pack(pady=20)

        # Output Label
        self.output_label = ttk.Label(root, text="Önerilen Film: ")
        self.output_label.pack(pady=10)

    def load_user_ids(self):
        unique_user_ids = df_new_rating['userId'].unique()
        for user_id in unique_user_ids:
            self.user_listbox.insert(tk.END, user_id)

    def toggle_user_listbox(self):
        if self.recommendation_type.get() == "personalized":
            self.user_listbox.config(state="normal")
        else:
            self.user_listbox.config(state="disabled")

    def show_genre_listbox(self):
        self.genre_listbox.pack()
        self.movie_listbox.pack_forget()

    def show_movie_listbox(self):
        if self.recommendation_type.get() == "popular":
            self.populate_movie_listbox(df_movie['movieId'])
            
        elif self.recommendation_type.get() == "personalized" and self.user_listbox.curselection() :
            #user_id = self.user_listbox.get(self.user_listbox.curselection()[0])
            if self.user_listbox.curselection():
                user_id = self.user_listbox.get(self.user_listbox.curselection()[0])
            else:
                messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı seçin.")   
            user_movies = df_new_rating[df_new_rating['userId'] == int(user_id)]['movieId']
            self.populate_movie_listbox(user_movies)
        self.genre_listbox.pack_forget()
        self.movie_listbox.pack()

    def populate_movie_listbox(self, movie_ids):
        self.movie_listbox.delete(0, tk.END)
        for movie_id in movie_ids:
            self.movie_listbox.insert(tk.END, movie_id)

    def recommend_movie(self):
        recommendation = "Film Seçimi yapılamadı."

        user_id = int(self.user_listbox.get(tk.ACTIVE))
        genre = self.genre_listbox.get(tk.ACTIVE)
        
        # POPÜLER
        # Popüler ve İsim
        if self.recommendation_type.get() == "popular" and self.search_type.get() == "title" and self.movie_listbox.curselection():
            movie = self.movie_listbox.get(self.movie_listbox.curselection()[0])
            consequents = searchNode(self.trie, frozenset([movie]))
            if consequents:
                recMovies = sorted(consequents, key=lambda x: x[2], reverse=True)
                recMovieId = next(iter(recMovies[0][0]))
                for index, row in df_popular_movie.iterrows():
                        if row['movieId'] == recMovieId:
                            self.output_label.config(text=f'{recMovieId}')
                            recommendation = f"Önerilen Film: {recMovieId}"
            else:
                recommendation = f"Önerilen Film: Popular Movie listesinde yok."


            
        
        # Popüler ve Kategori
        elif self.recommendation_type.get() == "popular" and self.search_type.get() == "genre" and self.genre_listbox.curselection():
            """"""
            genre = self.genre_listbox.get(self.genre_listbox.curselection()[0])
            all_movies = df_movie['movieId'].tolist()
            recMovieId = recommend_high_confidence_movie(self.trie,all_movies,genre)
            recommendation = f"Önerilen Film: {recMovieId}"
        
        # KİŞİSEL
        # Kişisel ve İsim
        elif self.recommendation_type.get() == "personalized" and self.search_type.get() == "title" and self.movie_listbox.curselection():
            """"""
            movie = self.movie_listbox.get(self.movie_listbox.curselection()[0])
            consequents = searchNode(self.trie, frozenset([movie]))
            if consequents:
                recMovies = sorted(consequents, key=lambda x: x[2], reverse=True)
                recMovieId = next(iter(recMovies[0][0]))
                recommendation = f"Önerilen Film: {recMovieId}"
            else:
                recommendation = f"{movie} filmine ait öneri bulunamadı."

            
        # Kişisel ve Kategori
        elif self.recommendation_type.get() == "personalized" and self.search_type.get() == "genre" :
            
            user_movies = df_new_rating[df_new_rating['userId'] == int(user_id)]['movieId']
            recMovieId = recommend_high_confidence_movie(self.trie,user_movies,genre)
            recommendation = f"Önerilen Film: {recMovieId}"
                    
        self.output_label.config(text=recommendation)


# Run the App
root = tk.Tk()
app = MovieRecommendationApp(root)
root.mainloop()
