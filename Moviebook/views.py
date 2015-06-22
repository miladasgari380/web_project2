from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Moviebook.models import *
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from .form import *

def logout_view(request):
    logout(request)
    return redirect('/login/')


def login(request):
    message = ''
    if request.method == "POST":

        form = LoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            print(username)
            print(password)

            # user = authenticate(username=username, password=password)
            user = authenticate(username = username, password = password)
            print(user)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/home/')
                else:
                    # not active user
                    message = "This user is deactivated"
            else:
                message = "Username or password is wrong"
        else:
            form = LoginForm()
    form = LoginForm()
    return render(request, "login.html", {
        'form': form,
        'message': message,
    })

def signup(request):
    message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['username'])
            new_user = Guest() #.objects.create_user(form.cleaned_data['username'],
                                                 # form.cleaned_data['email'],
                                                 # form.cleaned_data['password'])
            new_user.username = form.cleaned_data['username']
            new_user.password = form.cleaned_data['password']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.birthday = form.cleaned_data['birthday']
            new_user.gender = form.cleaned_data['gender']
            print((form.cleaned_data['birthday'], new_user.birthday))
            # try:
            new_user.save()
            # except:
                # pass
            message = "Successfully created"
    else:
        form = SignupForm()
        message = "Unsuccessful creation"
    return render(request, "signup.html", {
        'form': form,
        'message': message,
    })

@login_required(login_url='/login/')
def home(request):
    #una e ke followshun mikone
   # usr = request.user #not sure
    posts = Post.objects.all().order_by("-date")
    comments = Comment.objects.all().order_by("-date")
    likes = Like.objects.all()
    # for p in posts:
    #     comments = Comment.objects.filter(post=p).order_by("-date")
    #     dict[p.id] = comments.id
    # print(dict)
    return render(request, "home.html", {
        'posts': posts,
        # 'dict': dict,
        'comments': comments,
        'likes': likes,
    })


def show_post(request, post_id):
    post = Post.objects.get(id=post_id)
    # post = Post.objects.filter(owner=usr).get(id)
    return render(request, "post.html", {
        'post': post,
    })

def user_profile(request, user_name):
    try:
        usr = Guest.objects.get(username = user_name)
        followers = len(Follow.objects.filter(following = usr))
        following = len(Follow.objects.filter(follower = usr))
        posts = Post.objects.filter(owner = usr).order_by("date")

    except Guest.DoesNotExist:
        raise Http404

    return render(request, "user_profile.html", {
        'user': usr,
        'follower': followers,
        'following': following,
        'posts': posts
    })


def followers(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followers = Follow.objects.filter(following = usr)
    temp = [x.follower for x in followers]
    return render(request, "users_list.html", {
        'list': temp
    })


def followings(request, user_name):
    usr = Guest.objects.get(username = user_name)
    followings = Follow.objects.filter(follower = usr)
    temp = [x.following for x in followings]
    return render(request, "users_list.html", {
        'list': temp
    })

#
# def forgot(request, hash):
#     if len(Guest.objects.filter(forgot_hash=hash)):
#         return render(request, 'fucking_template.html')
#
#
# import hashlib
#
# def create_hash(request):
#     email = request.POST['email']
#     sha1 = hashlib.sha1()
#     sha1.update('salam')
#     print(sha1.digest())