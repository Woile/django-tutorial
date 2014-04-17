# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
#from django.http import HttpResponseRedirect, Http404
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm  # Form to create user
#from django.contrib.auth.views import login
from apps.blog.models import Post
from apps.blog.forms import PostForm
from apps.blog.forms import CommentForm, UserRegisterForm, PerfilUserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.blog.decorators import owner

#def home(request):
    #posts = Post.objects.all().order_by('-datetime')[:2]
    #return render(request, "blog/home.html", {'posts': posts})


def home(request):
    """Paginated 2 posts order by -datetime"""
    post_list = Post.objects.all().order_by('-datetime')
    paginator = Paginator(post_list, 2)  # 2 per page (for testing purpouses)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # delivers first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/home.html', {'posts': posts})


def create_user(request):
    """ Under development """
    form = UserRegisterForm(request.POST or None)
    #form2 = PerfilUserForm(request.POST or None)
    if form.is_valid(): #and form2.is_valid():
        psw = form.clean_password2()  # executes def inside UserRegisterForm
        new_user = form.save(commit=False)
        new_user.set_password(psw)
        new_user.save()
        #profile = form2.save(commit=False)
        #profile.user = new_user
        #profile.save()
        return redirect(reverse('login'))
    return render(request, 'registration.html', {'form': form}) #, 'form2': form2})


def posts(request):
    posts = Post.objects.all().order_by("-datetime")
    result = {}
    for p in posts:
        result[p] = p.comment_set.all()
    #posts = Post.objects.filter(title__startswith="C")
    return render(request, "blog/posts.html", {'posts': result})


def view_post(request, post_id):
    """View a single post, commenting DOES NOT requiere validation from author
    >>Must do: Author CAN remove comment"""
    post_instance = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        user = request.user
        comment = form.save(commit=False)
        comment.author = user
        comment.post = post_instance
        comment.save()
        return redirect(reverse("view_post", kwargs={'post_id': post_id}),
            {'post': post_instance, 'form': form})
    return render(request, "blog/view_post.html",
        {'post': post_instance, 'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None)  # Por qué or None?
    if form.is_valid():  # All validation rules pass
        user = request.user
        post = form.save(commit=False)
        post.author = user
        post.save()
        return redirect(reverse("blog_home"))

    return render(request, "blog/create_post.html", {'form': form})


@login_required
@owner
def edit_post(request, post_id):
    logging.critical(request.method)
    a_post_instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=a_post_instance)
    if form.is_valid():  # All validation rules pass
        form.save()
        return redirect(reverse("blog_posts"))

    return render(request, "blog/edit_post.html", {'form': form})


@login_required
def view_profile(request):
    return render(request, 'view_profile.html')


@login_required
def edit_profile(request):
    """under development"""
    user = request.user
    profile = user.get_profile()
    form2 = PerfilUserForm(request.POST or None, instance=profile)
    print "SAnti capooo"
    print form2.is_valid()
    if form2.is_valid():
        print form2.cleaned_data
        user.first_name = form2.cleaned_data['first_name']
        user.last_name = form2.cleaned_data['last_name']
        user.save()
        profile.genre = form2.cleaned_data['genre']
        profile.birth_date = form2.cleaned_data['birth_date']
        profile.save()
        return redirect(reverse("view_profile"))
    return render(request, "edit_profile.html", {'form': form2})

# ---------------------------------------------------
# FORMS EXAMPLES
# ---------------------------------------------------


#def create_post_first_aproach(request):

    #if request.method == "POST":
        #form = PostForm(request.POST)  # A form bound to the POST data
        #if form.is_valid():  # All validation rules pass
            ## Process the data in form.cleaned_data
            ## ...
            #user = User.objects.all()[0]
            #post = form.save(commit=False)
            #post.author = user
            #post.save()
            #return redirect(reverse("blog_posts"))  # Redirect after POST
    #else:
        #form = PostForm()

    #return render(request, "blog/create_post.html", {'form': form})

