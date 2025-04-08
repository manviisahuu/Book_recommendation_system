from django.contrib import admin
from django.urls import path
from books import views  # Import all views from books/views.py

urlpatterns = [
    # Core Pages
    path("", views.home, name="home"),  # Homepage
    path("home/", views.home, name="home"),
    path("books/", views.books_page, name="books"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login_view, name="login"),
    path("recommendations/", views.recommendations_page, name="recommendation"),  # Recommendation page
    path("api/books/", views.books_list, name="books_list"),
    path("api/recommend/", views.recommend_book, name="recommend_book"),
    path("check_book_exists/", views.check_book_exists, name="check_book_exists"),  
    #  API Endpoints
    path('search-results/', views.search_results, name='search_results'),
    path("search-suggestions/", views.search_suggestions, name="search_suggestions"),
    path("recommend/", views.recommend_book, name="recommend_book"),  # Book recommendation API
    path("get_recommendations/", views.recommend_book, name="get_recommendations"),  # Alternate API route
    path("book_list/", views.books_list, name="book_list"),  # API for all books

    # Django Admin Panel
    path("admin/", admin.site.urls),
]

