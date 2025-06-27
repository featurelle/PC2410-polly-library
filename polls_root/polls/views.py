from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models


def index(request):
    questions = models.Question.objects.order_by('-views', '-pub_date')
    context = {
        'questions': questions
    }
    return render(request, template_name='polls/index.html', context=context)


def detail(request, pk: int):
    question = models.Question.visit(pk)
    options = question.options.all()
    context = {
        'question': question,
        'options': options
    }
    return render(request, template_name='polls/detail.html', context=context)


def vote(request, pk: int):
    choice_pk = request.POST.get('choice-pk')
    question = models.Question.get(pk)
    question.vote(choice_pk)
    return HttpResponseRedirect(reverse('polls:results', kwargs={'pk': pk}))


def vote_own(request, pk: int):
    choice_text = request.POST.get('choice-own')
    question = models.Question.get(pk)
    option = question.add_option(choice_text)
    question.vote(option.pk)
    return HttpResponseRedirect(reverse('polls:results', kwargs={'pk': pk}))


def results(request, pk: int):
    question = models.Question.get(pk)
    options = question.options.all()
    context = {
        'question': question,
        'options': options
    }
    return render(request, template_name='polls/results.html', context=context)
