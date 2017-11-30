from django.contrib.auth.models import User

from django.shortcuts import render,redirect

from django.http import HttpResponse,Http404

from .models import Board,Topic,Post
from .forms import NewTopicForm
# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request , 'home.html' , {'boards':boards})

def board_topics(request , pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request , 'topic.html' , {'board':board} )

def new_topic(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404

    if request.method=='POST':
        user = User.objects.first()
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create( message=form.cleaned_data.get('message') , topic=topic, created_by=user)
            return redirect('board_topics' ,pk = board.pk)

    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board ,'form':form})