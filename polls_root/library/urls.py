from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    # site
    path('', view=views.index, name='index'),
    path('books/', view=views.books, name='books'),
    path('authors/', view=views.authors, name='authors'),
    path('genres/', view=views.genres, name='genres'),
    path('books/<int:pk>', view=views.book_details, name='book'),
    path('books/<int:pk>/comment', view=views.comment_book, name='comment-book'),
    path('books/<int:book_pk>/copies', view=views.book_copies, name='copies'),
    path('books/copies/<int:pk>/loan', view=views.set_copy_loan, name='set-loan'),
    path('books/copies/<int:pk>/free', view=views.unset_copy_loan, name='unset-loan'),
    path('authors/<int:pk>', view=views.author_details, name='author'),
    path('genres/<int:pk>', view=views.genre_details, name='genre'),

    # api
    path('api/v1/books/list', view=views.BookListAPIView.as_view(), name='api-book-list'),
    path('api/v1/authors/list', view=views.AuthorListAPIView.as_view(), name='api-author-list'),


]
