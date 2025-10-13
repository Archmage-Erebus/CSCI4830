from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Score
from .forms import ScoreForm

def hello(request):
    return HttpResponse("Hello World!!!!")

def index(request): 
    return render(request, 'index_hello.html')

def about(request): 
    return render(request, 'about_hello.html')

def score_view(request):
    scores = Score.objects.all()
    
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('score_view')
    else:
        form = ScoreForm()

    return render(request, 'score_list.html', {'form': form, 'scores': scores})

def edit_score(request, score_id): 
    score = get_object_or_404(Score, id=score_id)

    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            return redirect('score_view')
    else:
        form = ScoreForm(instance=score)
    
    return render(request, 'score_edit.html', {'form': form, 'score': score})

def delete_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    score.delete()
    return redirect('score_view')
# Create your views here.