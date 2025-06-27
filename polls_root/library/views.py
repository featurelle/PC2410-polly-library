from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from rest_framework import generics

from . import models
from . import serializers


def index(request):
    context = {
        'books_count': models.Book.objects.count(),
        'authors_count': models.Author.objects.count(),
        'genres_count': models.Genre.objects.count(),
    }
    return render(request, template_name='library/index.html', context=context)


def authors(request):
    context = {
        'authors': models.Author.objects.all()
    }
    return render(request, template_name='library/authors/index.html', context=context)


def books(request):
    context = {
        'books': models.Book.objects.prefetch_related('author')
    }
    return render(request, template_name='library/books/index.html', context=context)


def genres(request):
    books_set = models.Book.objects.prefetch_related('author')
    genres_set = models.Genre.objects.prefetch_related(Prefetch('books', queryset=books_set))
    context = {
        'genres': genres_set
    }
    return render(request, template_name='library/genres/index.html', context=context)


def author_details(request, pk: int):
    author = models.Author.objects.prefetch_related('books').get(pk=pk)
    author_books = author.books.prefetch_related('genres')
    author_genres = author.genres
    comments = author.comments
    context = {
        'author': author,
        'books': author_books,
        'genres': author_genres,
        'comments': comments
    }
    return render(request, template_name='library/authors/detail.html', context=context)


def book_details(request, pk: int):
    book = models.Book.objects.prefetch_related('genres', 'comments').get(pk=pk)
    book_author = book.author
    book_genres = book.genres.all()
    book_comments = book.comments.all()
    context = {
        'book': book,
        'author': book_author,
        'genres': book_genres,
        'comments': book_comments
    }
    return render(request, template_name='library/books/detail.html', context=context)


def book_copies(request, book_pk: int):
    context = {
        'book': models.Book.objects.prefetch_related('copies').get(pk=book_pk)
    }
    return render(request, template_name='library/books/copies.html', context=context)


def set_copy_loan(request, pk: int):
    client = request.POST.get('client')
    duedate = request.POST.get('duedate')
    book_copy = models.BookCopy.objects.get(pk=pk)
    book_copy.status = 'o'
    book_copy.client = client
    book_copy.duedate = duedate
    book_copy.save()
    return HttpResponseRedirect(reverse('library:copies', kwargs={'book_pk': book_copy.book.pk}))


def unset_copy_loan(request, pk: int):
    book_copy = models.BookCopy.objects.get(pk=pk)
    book_copy.status = 'a'
    book_copy.client = None
    book_copy.duedate = None
    book_copy.save()
    return HttpResponseRedirect(reverse('library:copies', kwargs={'book_pk': book_copy.book.pk}))


def genre_details(request, pk: int):
    return HttpResponseRedirect(reverse('library:genres') + f'#genre-{pk}')


def comment_book(request, pk: int):
    author = request.POST.get('comment-author')
    text = request.POST.get('comment-text')
    models.Book.objects.get(pk=pk).comment(author, text)
    return HttpResponseRedirect(reverse('library:book', kwargs={'pk': pk}))


class BookListAPIView(generics.ListAPIView):
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.prefetch_related('genres', 'comments', 'author')


class AuthorListAPIView(generics.ListAPIView):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.prefetch_related('books')

