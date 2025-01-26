import pytest
import pandas as pd
from unittest.mock import MagicMock
import tkinter as tk
from tkinter import messagebox
from graphic_ui import MovieRecommendationApp  # Uygulama kodunuzun doğru import edilmesi gerek

# Veri çerçevelerinin örnek olarak tanımlanması
@pytest.fixture
def setup_app():
    root = tk.Tk()
    app = MovieRecommendationApp(root)
    return app

# Mocking the pandas dataframes used in the app (since the real df is not available)
@pytest.fixture
def mock_dataframes():
    mock_df_movie = pd.DataFrame({
        'movieId': [1, 2, 3],
        'title': ['Movie A', 'Movie B', 'Movie C'],
        'genres': ['Action', 'Comedy', 'Drama']
    })
    mock_df_new_rating = pd.DataFrame({
        'userId': [101, 102],
        'movieId': [1, 2],
        'rating': [5, 4],
        'timestamp': [20240101, 20240102]
    })
    mock_df_popular_movie = pd.DataFrame({
        'movieId': [1, 2],
        'title': ['Movie A', 'Movie B'],
        'rating': [4.5, 3.8]
    })

    return mock_df_movie, mock_df_new_rating, mock_df_popular_movie

# Test: `load_user_ids` fonksiyonu çalışacak şekilde userId'lerin eklenip eklenmediğini kontrol etme
def test_load_user_ids(setup_app, mock_dataframes):
    app = setup_app
    mock_df_movie, mock_df_new_rating, mock_df_popular_movie = mock_dataframes

    # Mocking df_new_rating
    app.df_new_rating = mock_df_new_rating

    # Veritabanına kullanıcı ID'lerini ekle
    app.load_user_ids()
    
    # Listbox'ta doğru sayıda kullanıcı olmalı
    assert app.user_listbox.size() == len(mock_df_new_rating['userId'].unique())
    assert app.user_listbox.get(0) == 101  # İlk kullanıcıyı kontrol et

# Test: `populate_movie_listbox` fonksiyonu çalışacak şekilde film listelerinin doğru şekilde popüle edilip edilmediğini kontrol etme
def test_populate_movie_listbox(setup_app, mock_dataframes):
    app = setup_app
    mock_df_movie, mock_df_new_rating, mock_df_popular_movie = mock_dataframes

    # Popüler filmleri listele
    app.populate_movie_listbox(mock_df_movie['movieId'])
    
    # Listbox'ta doğru sayıda film olmalı
    assert app.movie_listbox.size() == len(mock_df_movie['movieId'])
    assert app.movie_listbox.get(0) == 1  # İlk film ID'sini kontrol et

# Test: `recommend_movie` fonksiyonunun doğru çalışıp çalışmadığını kontrol etme
def test_recommend_movie(setup_app, mock_dataframes):
    app = setup_app
    mock_df_movie, mock_df_new_rating, mock_df_popular_movie = mock_dataframes

    # Verileri mockla
    app.df_new_rating = mock_df_new_rating
    app.df_movie = mock_df_movie
    app.df_popular_movie = mock_df_popular_movie

    # Popüler öneri (film ismi) yapmak için fonksiyonu çalıştır
    app.recommendation_type.set("popular")
    app.search_type.set("title")
    app.movie_listbox.select_set(0)  # İlk filmi seç

    # Fonksiyonun doğru çalışıp çalışmadığını kontrol et
    app.recommend_movie()
    assert app.output_label.cget("text") == "Önerilen Film: 1"  # Önerilen film ID'si kontrol et

    # Kişisel öneri (film ismi) yapmak için fonksiyonu çalıştır
    app.recommendation_type.set("personalized")
    app.search_type.set("title")
    app.user_listbox.select_set(0)  # İlk kullanıcıyı seç

    app.recommend_movie()
    assert app.output_label.cget("text") != "Film Seçimi yapılamadı."  # Öneri yapılmalı

# Test: Film türüne göre öneri
def test_recommend_by_genre(setup_app, mock_dataframes):
    app = setup_app
    mock_df_movie, mock_df_new_rating, mock_df_popular_movie = mock_dataframes

    # Verileri mockla
    app.df_new_rating = mock_df_new_rating
    app.df_movie = mock_df_movie
    app.df_popular_movie = mock_df_popular_movie

    # Film türüne göre öneri yapmak için fonksiyonu çalıştır
    app.recommendation_type.set("popular")
    app.search_type.set("genre")
    app.genre_listbox.select_set(0)  # İlk türü seç

    app.recommend_movie()
    assert app.output_label.cget("text") == "Önerilen Film: 1"  # Önerilen film ID'si kontrol et

