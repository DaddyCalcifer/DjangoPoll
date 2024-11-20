from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice

def index(request):
    questions = Question.objects.all()
    return render(request, 'survey/index.html', {'questions': questions})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'survey/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'survey/detail.html', {
            'question': question,
            'error_message': "Выберите вариант ответа.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('index')
