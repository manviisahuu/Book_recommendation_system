from books.recommender import get_similar_books

# Choose a book index to get recommendations
book_index = 100  # Change this to test different books

# Get recommended books
recommended_books = get_similar_books(book_index)

# Display recommendations
print("\n📚 Recommended Books:")
if recommended_books:
    for book in recommended_books:
        print(f"📖 Title: {book['title']}, ✍️ Author: {book['author']}, 🔗 Similarity Score: {book['similarity_score']:.4f}")
else:
    print("⚠️ No recommendations found. Check if the book index is valid!")

