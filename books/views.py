from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from .models import Book


# Load the dataset
CSV_PATH = "C:/Users/DELL/Documents/book_recommendation_system/bookrec/final_cleaned_books_updated2.csv"
books_df = pd.read_csv(CSV_PATH)


#  Convert selected books to JSON format
books_page_df = books_df.head(100)# Use full dataset (not filtered)
books_list_for_page = books_page_df[["book_title", "book_author", "year_of_publication", "image_url"]].to_dict(orient="records")


#  Handle Missing Publisher Values
books_df["publisher"] = books_df["publisher"].fillna("N/A")

#  Combine relevant features for content-based filtering
books_df["combined_features"] = books_df["book_title"].astype(str) + " " + \
                                books_df["book_author"].astype(str) + " " + \
                                books_df["publisher"].astype(str)

#  Convert text data into numerical vectors using TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2), min_df=2)
tfidf_matrix = tfidf.fit_transform(books_df["combined_features"])

#  Fit Nearest Neighbors model
nn_model = NearestNeighbors(n_neighbors=6, metric="cosine", algorithm="brute")
nn_model.fit(tfidf_matrix)

#  Function to Get Similar Books
def get_similar_books(title, num_recommendations=5):
    matches = books_df[books_df["book_title"].str.lower().str.strip() == title.lower().strip()]
    #book_indices = books_df[books_df["book_title"].str.lower().str.strip() == title.lower().strip()].index

    if matches.empty:
        return []

    book_index = matches.index[0]

    try:
        distances, indices = nn_model.kneighbors(tfidf_matrix[book_index], n_neighbors=num_recommendations + 1)
    except IndexError:
        return []
    #if len(book_indices) == 0:
     #   return []

    #book_index = book_indices[0]
    #distances, indices = nn_model.kneighbors(tfidf_matrix[book_index], n_neighbors=num_recommendations + 1)

    recommendations = []
    seen_titles = set()

    for idx, score in zip(indices[0][1:], distances[0][1:]):  # Exclude input book itself
        if idx >= len(books_df):
            continue

        book_info = books_df.iloc[idx]
        book_title = book_info["book_title"]
    #book_title = books_df.iloc[idx]["book_title"]
     #   author = books_df.iloc[idx]["book_author"]
      #  similarity = round((1 - score) * 100, 2)  # Convert to percentage

       # image_url = books_df.iloc[idx]["image_url"]
       # publisher = books_df.iloc[idx]["publisher"]

        if book_title in seen_titles:
            continue

        recommendations.append({
                "title": book_info["book_title"],
                "author": book_info["book_author"],
                "publisher": book_info["publisher"],
                "similarity_score": round((1 - score) * 100, 2),  # Store as float
                "image_url": book_info["image_url"]
            })
        seen_titles.add(book_title)

        if len(recommendations) == num_recommendations:
            break

    return recommendations

#  Render Pages
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def books_page(request):
    all_books = Book.objects.only('book_title', 'book_author', 'image_url', 'year_of_publication') 
    paginator = Paginator(all_books, 20)  # Show 20 books per page

    page_number = request.GET.get('page')
    page_books = paginator.get_page(page_number)
    return render(request, "books.html", {"page_books": page_books})

def contact(request):
    return render(request, "contact.html")

def login_view(request):
    return render(request, "login.html")

def recommendations_page(request):
    return render(request, 'recommendations.html')  #  Fixed template name

def books_list(request):
    return JsonResponse({"books": books_list_for_page})  # Send the books JSON data

def recommend_book(request):
    if request.method == "GET":
        book_title = request.GET.get("book_title", "").strip()
        print(f"Requested book title: {book_title}") 

    if not book_title:
        print("Book title is missing!")
        return JsonResponse({"error": "Book title is required"}, status=400)
    

    matched_books = books_df[books_df["book_title"].str.lower().str.strip() == book_title.lower().strip()]

    if matched_books.empty:
        print("Book not found in dataset.")
        return JsonResponse({"error": "Book not found. Please check the title."}, status=404)

    try:
        recommendations = get_similar_books(book_title)
        print(f"Generated {len(recommendations)} recommendations.")
    except Exception as e:
        print(f"Exception during recommendation: {str(e)}") 
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)


    return JsonResponse({"recommendations": recommendations})

    return JsonResponse({"error": "Invalid request method."}, status=405)

def check_book_exists(request):
    title = request.GET.get("title", "")
    exists = not books_df[books_df["book_title"].str.lower().str.strip() == title.lower().strip()].empty
    return JsonResponse({"exists": exists})


def search_results(request):
    query = request.GET.get("query", "").strip()
    matched_book = books_df[books_df["book_title"].str.lower().str.strip() == query.lower()]

    if matched_book.empty:
        return render(request, "search.html", {
            "book": None
        })

    book_data = matched_book.iloc[0]
    return render(request, "search.html", {
        "book": {
            "title": book_data["book_title"],
            "author": book_data["book_author"],
            "publisher": book_data["publisher"],
            "year": book_data["year_of_publication"],
            "image_url": book_data["image_url"] or "/static/images/default-cover.jpg"
        }
    })


def search_suggestions(request):
    query = request.GET.get("query", "").lower()
    suggestions = []

    if query:
        matched_books = books_df[books_df["book_title"].str.lower().str.contains(query, na=False)]
        suggestions = matched_books["book_title"].dropna().unique().tolist()[:10]

    return JsonResponse({"suggestions": suggestions})
  