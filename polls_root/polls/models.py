from django.db import models
from django.utils import timezone


class Question(models.Model):
    title = models.TextField(unique=True)
    views = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)

    @property
    def votes(self) -> int:
        return sum(option.votes for option in self.options.all())

    @classmethod
    def get(cls, pk: int | str) -> 'Question':
        return cls.objects.get(id__exact=pk)

    @classmethod
    def visit(cls, pk: int | str) -> 'Question':
        question = cls.get(pk)
        question.views += 1
        question.save(update_fields=['views'])
        return question

    def vote(self, option_pk: int | str):
        option = self.options.get(id__exact=option_pk)
        option.votes += 1
        option.save()

    def add_option(self, text: str) -> 'Option':
        option = Option(text=text, question=self)
        option.save()
        return option

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.question}: {self.text}'
