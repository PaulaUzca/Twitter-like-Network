import json
from django.contrib.auth import authenticate, login, logout
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db.utils import Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , resolve_url
from django.urls import reverse
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.decorators.http import require_GET, require_POST
from django.template.loader import render_to_string

from django.core.paginator import Paginator
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse


from django.views.decorators.csrf import csrf_exempt

from itertools import chain
from operator import attrgetter


from .models import Follow, User, Post, Like

def getPost(id):
    try:
        post = Post.objects.get(id = id)
    except Error:
        raise HttpResponseBadRequest
    else:
        return post


def getPostLikes(post):
    return Like.objects.filter(post = post).count()

# check if user likes a specific post
def doesUserLike(user,post):
    try:
        Like.objects.get(post = post, user=user)
    except ObjectDoesNotExist:
        return False
    else:
        return True

#check if user is following this account
def isUserFollowing(user, other):
    try:
        Follow.objects.get(user= user, user_follow=other)
    except ObjectDoesNotExist:
        return False
    else:
        return True

#check if this account is following the user
def isAccountFollower(user, other):
    try:
        Follow.objects.get(user = other, user_follow = user)
    except ObjectDoesNotExist:
        return False
    else:
        return True




#get all posts
@require_GET
def index(request):
    if request.GET.get('page'):
        #add annotation: create a variable for post likes that's more accesible from template
        posts = Post.objects.annotate(like_count = Count('likes')).order_by('-date').all() # in index it shows all posts in the app
        return getposts(request, posts)
    else:
        return render(request, "network/index.html")

#get follower posts
@login_required
def following(request):
    if request.GET.get('page'):
        posts = []
        for follow  in request.user.following.all():
           posts =  chain(posts, follow.user_follow.posts.all())

        posts = sorted(posts, key=attrgetter('date'), reverse= True)
        return getposts(request, posts)
    else:
        return render(request, "network/following.html")


# the post parameter comes from the index and following functions.
# it is the array of posts to get the posts from
def getposts(request, posts):
    p = Paginator(posts, 10)
    num_page = int(request.GET.get('page', 1))

    prev = 0
    next = 0

    if p.num_pages < num_page:
        raise HttpResponseBadRequest

    else:
        someposts = p.page(num_page)
        someposts_likes = []

        if request.user.is_authenticated:
            for post in someposts.object_list:
                if doesUserLike(request.user, post):
                    someposts_likes.append(post.id)

        if num_page < p.num_pages:
            next = someposts.next_page_number()
        
        if num_page > 1:
            prev = someposts.previous_page_number()
        
        rendered_posts = render_to_string('network/posts.html', context={'page':someposts, 'userlikes': someposts_likes})
        return JsonResponse({"posts": rendered_posts, "next": next, "prev": prev, "page":num_page})


def getOnePost(request, id):
    post =  Post.objects.get(id=id)

    if request.method == 'GET':
        data = {
            'post': post,
            'likes': getPostLikes(post),
            'userlike': doesUserLike(request.user, post)
        }
        return render(request,'network/onepost.html', data)

    elif request.method == 'PUT' and request.user == post.author:
        data = json.loads(request.body)
        new_content = data.get('newcontent')
        print(new_content)
        post.content = new_content
        post.edited = True
        print(post)
        try:
            post.save()
        except:
            return Http404
        else:
            return HttpResponse(200)
        
    elif request.method == 'DELETE' and request.user == post.author:
        try:
            post.delete()
        except:
            return Http404()
        else:
            return HttpResponse(200)



def likeManager(request):
    postid = json.loads(request.body).get('postid') #get the liked or disliked post id from the request
    post = getPost(postid)

    if request.method == 'PUT': # like - create new like object
        newLike = Like(post = post, user=request.user) 
        try:
            newLike.full_clean() # see if everything is ok when creating object
        except ValidationError:
            raise HttpResponseBadRequest
        else:
            newLike.save()

    elif request.method == 'DELETE': # dislike - delete like object 
        try:
            dislike = Like.objects.get(post= post, user=request.user)
        except ObjectDoesNotExist:
            raise HttpResponseBadRequest
        else:
            dislike.delete()

    return JsonResponse({'likes': getPostLikes(post) }, status=200)



@require_POST
def newpost(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        content = data.get('content')
        try: 
            Post.objects.newPost(request.user,content)
        except ValidationError:
            HttpResponse(500, content={'message':'post unsuccessful'})
        else:
            return HttpResponse(200)


def profile(request, username):
    user_profile = User.objects.get(username = username)

    if request.method == 'PUT':
        try:
            Follow.objects.get(user = request.user, user_follow= user_profile)
        
        except ObjectDoesNotExist: #follow user
            Follow.objects.follow(request.user, user_profile)
            return JsonResponse({'follow':True}, status=200)

        else: #unfollow user
            Follow.objects.unfollow(request.user, user_profile)
            return JsonResponse({'follow':False}, status=200)
        
    else:
        if request.GET.get('page'):
            posts = Post.objects.filter(author = user_profile)
            posts = posts.annotate(like_count = Count('likes')).order_by('-date')
            return getposts(request,posts)

        else: #just return the page
            profile = {
                'username' : user_profile.username,
                'followers_count' : user_profile.followers.count(),
                'following_count' : user_profile.following.count(),
                'userIsFollower' : isUserFollowing(request.user, user_profile),
                'followsUser' : isAccountFollower(request.user, user_profile)
            }
            return render(request, 'network/profile.html', profile)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
