import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

#  Set Correct File Path
CSV_PATH = "C:/Users/DELL/Documents/book_recommendation_system/bookrec/final_cleaned_books_updated2.csv"

# Load the dataset
books_df = pd.read_csv(CSV_PATH)

#  Combine relevant text features for content-based filtering
books_df["combined_features"] = (
    books_df["book_title"] + " " + books_df["book_author"] + " " + books_df["publisher"]
)

# Convert text data into numerical vectors using TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2), min_df=2)
tfidf_matrix = tfidf.fit_transform(books_df["combined_features"])

# Fit Nearest Neighbors model (Efficient Cosine Similarity Search)
nn_model = NearestNeighbors(n_neighbors=6, metric="cosine", algorithm="brute")
nn_model.fit(tfidf_matrix)


# Function to Get Similar Books
def get_similar_books(book_title, num_recommendations=5):
    # Check if the book exists
    if book_title not in books_df['book_title'].values:
        return []  # Return empty list if book not found

    book_index = books_df[books_df['book_title'] == book_title].index[0]
    distances, indices = nn_model.kneighbors(tfidf_matrix[book_index], n_neighbors=num_recommendations + 10)


    recommendations = []
    seen_titles = set() 
    for idx, score in zip(indices[0][1:], distances[0][1:]):  # Exclude the book itself
        title = books_df.iloc[idx]["book_title"]
        author = books_df.iloc[idx]["book_author"]
        similarity = round(1 - score, 4)

        if title not in seen_titles:  # Add only unique titles
            recommendations.append({"title": title, "author": books_df.iloc[idx]["book_author"], "similarity_score": similarity})
            seen_titles.add(title)  # Mark this title as seen

        if len(recommendations) == num_recommendations:  # Stop when we reach the required number
            break

    

    return recommendations


# Testing the function (Run this only for debugging, remove in production)
if __name__ == "__main__":
    test_title = "The Alchemist"
    print(f"\n Recommendations for Book Title: {test_title}")
    recommendations = get_similar_books(test_title)

    for book in recommendations:
        print(f" {book['title']} |  {book['author']} |  Similarity Score: {book['similarity_score']}")
