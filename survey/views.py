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
    
def stats(request):
    questions = Question.objects.all()
    stats_data = []

    for question in questions:
        total_votes = sum(choice.votes for choice in question.choices.all())
        choices_stats = [
            {
                'text': choice.text,
                'votes': choice.votes,
                'percentage': (choice.votes / total_votes * 100) if total_votes > 0 else 0,
            }
            for choice in question.choices.all()
        ]
        stats_data.append({
            'question': question,
            'total_votes': total_votes,
            'choices': choices_stats,
        })

    return render(request, 'survey/stats.html', {'stats_data': stats_data})

