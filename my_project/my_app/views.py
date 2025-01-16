from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Reply, Rating
from .forms import LoginForm, PostForm, CommentForm, ReplyForm, RatingForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
        
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_log = authenticate(request, username=username, password=password)
        
        if user_log is not None:
            login(request, user_log)  
            return redirect('home')  
        else:
            error_message = "Неверное имя пользователя или пароль."
            return render(request, 'login.html', {'error': error_message})

    return render(request, 'login.html')    
            
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts':posts})

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    ratings = post.ratings.all()
    new_comments = []
    for comment in comments:

        replies = Reply.objects.filter(comment=comment)

        dict_of_comment = {
            'id': comment.id,
            'author': comment.author,
            'post': comment.post,
            'content': comment.content,
            'replies': replies
        }
        new_comments.append(dict_of_comment)
        
        

    return render(request, 'post.html', {'post': post, 'comments': new_comments, 'ratings': ratings})

@csrf_exempt
def create_post(request):

    if request.method=="POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post', post_id=post.id)
    else:
        form = PostForm()
 
    return render(request, 'create_post.html')


@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'create_post.html', {'form': form})

@csrf_exempt
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('home')

@csrf_exempt
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ratings = post.ratings.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'comm.html', {'post':post, 'form': form, })

@csrf_exempt
def delete_comment(request, comment_id):
    comment=get_object_or_404(Comment, id=comment_id)
    if request.user==comment.author:
        comment.delete()
        return redirect('post', post_id=comment.post.id)
    else:
        return redirect('post', post_id=comment.post.id)



@csrf_exempt
def add_reply(request, comment_id):
    comment=get_object_or_404(Comment, id=comment_id)
    post_id=comment.post.id
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('post', post_id=comment.post.id)
    else:
        form = ReplyForm()

    return render(request, 'reply.html', {'post':post_id, 'comment': comment, 'form':form})

def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.user == reply.user:
        reply.delete()
        return redirect('post', post_id=reply.comment.post.id)
    else:
        return redirect('post', post_id=reply.comment.post.id)
    
def rating_for_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ratings = post.ratings.all() 

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.post = post
            rating.user = request.user
            rating.save()
            return redirect('post', post_id=post.id)
    else:
        form = RatingForm()
    print(ratings)
    return render(request, 'post.html', {'post': post, 'form': form, 'ratings': ratings})

def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id )
    if request.user == rating.user:
        rating.delete()
        return redirect('post', post_id = rating.post.id)
    else:
        return redirect('post', post_id = rating.post.id)






            


