import datetime
import random
from unittest import loader
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.http import HttpResponseRedirect
from django.shortcuts import render


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST[ 'choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    name = request.GET['question']
    return HttpResponse(template.render(context, request, './index.html', {'question': name}))


"""для кнопки"""
def question_page(request):
    question = request.GET['question']
    return render(request, './test.html', {'question' : question})




def n_q(request):
    if request.method == "GET":
        template_name = 'polls/test.html'
        return TemplateResponse(request, template='polls/test.html')
    elif request.method == "POST":
        inputtxt = request.POST.get["question"]
        new_question = Question()
        new_question.question_text = str(inputtxt)
        new_question.pub_date = datetime.datetime.now()
        new_question.save()

        return HttpResponseRedirect(reverse('polls:index'))


def n_q_T(request):

    if request.method == "GET":
        template_name = 'polls/test.html'
        return TemplateResponse(request, template='polls/test.html')
    elif request.method == "POST":
        print("This is post request")
        return HttpResponseRedirect(reverse('polls:index'))
