from rest_framework import serializers

from . import models


class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'first', 'last', 'img')


class BookBookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookComment
        fields = ('id', 'author', 'text', 'datetime')


class BookSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField()
    # author = serializers.SlugRelatedField(slug_field='last', read_only=True)
    author = BookAuthorSerializer()
    comments = BookBookCommentSerializer(many=True)
    genres = BookGenreSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ('id', 'title', 'author', 'genres', 'cover', 'comments')


class AuthorBookSerializer(serializers.ModelSerializer):
    comments = BookBookCommentSerializer(many=True)
    genres = BookGenreSerializer(many=True)

    class Meta:
        model = models.Book
        fields = ('id', 'title', 'genres', 'cover', 'comments')


class AuthorSerializer(serializers.ModelSerializer):
    books = AuthorBookSerializer(many=True)

    class Meta:
        model = models.Author
        fields = ('id', 'first', 'last', 'birth', 'death', 'dead', 'books')
