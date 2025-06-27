from django.contrib import admin

from . import models


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'genres_list')
    list_display_links = ('title',)

    @admin.display(description='genres')
    def genres_list(self, book):
        return list(book.genres.all())


@admin.register(models.BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'status', 'client', 'duedate')
    list_display_links = ('book_title',)
    ordering = ('book__title',)

    @admin.display(description='book')
    def book_title(self, copy):
        return copy.book.title


@admin.register(models.BookComment)
class BookCommentAdmin(admin.ModelAdmin):
    pass
