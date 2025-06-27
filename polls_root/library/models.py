from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(max_length=64)
    # books

    def __repr__(self):
        return f'<{self.__class__.__name__}: "{self.name}">'

    def __str__(self):
        return self.name


class Author(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    birth = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    dead = models.BooleanField(null=True, blank=True)
    img = models.URLField(null=True, blank=True)
    # books

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(birth__gt=timezone.now()),
                name='born_in_past',
                violation_error_message='Author can\'t be born in future'
            ),
            models.CheckConstraint(
                check=~models.Q(death__gt=timezone.now()),
                name='died_in_past',
                violation_error_message='You can\'t set author\'s death in future'
            ),
            models.CheckConstraint(
                check=models.Q(death__gt=models.F('birth')),
                name='died_after_birth',
                violation_error_message='Author couldn\'t die the day he/she was born or earlier'
            ),
            models.CheckConstraint(
                check=models.Q(
                    death__isnull=False, dead__isnull=False, dead__exact=True
                ) | models.Q(death__isnull=True),
                name='died_n_dead',
                violation_error_message='Author can\'t have the date of death if not dead'
            )
        ]

    def __repr__(self):
        return f'<{self.__class__.__name__}: "{self.fullname}">'

    def __str__(self):
        return self.fullname

    @property
    def fullname(self) -> str:
        return f'{self.first} {self.last}'

    @property
    def genres(self) -> QuerySet[Genre]:
        return Genre.objects.filter(books__author=self)

    @property
    def comments(self) -> QuerySet['BookComment']:
        return BookComment.objects.filter(book__author=self)


class Book(models.Model):
    title = models.CharField(max_length=256)
    about = models.TextField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    # copies
    # comments

    def __repr__(self):
        return f'{self.__class__.__name__}: "{self.title}"'

    def __str__(self):
        return f'{self.title}, by {self.author.fullname}'

    def comment(self, author: str, text: str) -> 'BookComment':
        comment = BookComment(author=author, text=text, book=self)
        comment.save()
        return comment


class BookCopy(models.Model):

    _STATUSES = (
        ('a', 'available'),
        ('m', 'maintenance'),
        ('o', 'on loan'),
        ('r', 'reserved'),
        ('l', 'lost')
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    status = models.CharField(max_length=1, default='a', choices=_STATUSES)
    client = models.CharField(max_length=64, null=True, blank=True)
    duedate = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "book copies"
        constraints = [
            models.CheckConstraint(
                check=models.Q(status='o', client__isnull=False, duedate__isnull=False)
                | (~models.Q(status='o') & models.Q(client__isnull=True, duedate__isnull=True)),
                name='no_partial_loan_info',
                violation_error_message='Partial loan info (only status, client or duedate)'
                                        ' is not accepted. Either set all loan-related fields or none'
            )
        ]

    def __repr__(self):
        return f'{self.__class__.__name__}: "{self.book.title}" ({self.id} > {self.status})'

    def __str__(self):
        return f'Copy of "{self.book.title}" (id: {self.id})'


class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=64)
    text = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-datetime',)

    def __repr__(self):
        return f'{self.__class__.__name__}: on Book "{self.book.title}" (id: {self.id}, dt: {self.datetime})'

    def __str__(self):
        return f'Comment: "{self.text}" ({self.book.title})'
