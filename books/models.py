from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True, default="Unknown")  # Changed `ISBN` → `isbn`
    book_title = models.CharField(max_length=255, default="Unknown")  # Changed `Book-Title` → `book_title`
    book_author = models.CharField(max_length=255, default="Unknown")  # Changed `Book-Author` → `book_author`
    year_of_publication = models.IntegerField(default=2000)  # Changed `Year-Of-Publication` → `year_of_publication`
    publisher = models.CharField(max_length=255, default="Unknown")  # Changed `Publisher` → `publisher`
    image_url = models.URLField(blank=True, null=True, default="")  # Changed `Image-URL` → `image_url`

    def __str__(self):
        return self.book_title  # Use corrected field name



