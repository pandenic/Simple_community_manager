"""Contain page renders for posts app."""
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post, Group, Follow
from posts.forms import PostForm, CommentForm
from yatube.settings import (
    MAX_POSTS_PER_PAGE,
    MAX_COMMENTS_PER_PAGE,
    INDEX_CACHING_TIME_SEC,
)

User = get_user_model()


def make_pagination_obj(request, obj_list, obj_per_page):
    """Paginator creation function."""
    paginator = Paginator(obj_list, obj_per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


@cache_page(INDEX_CACHING_TIME_SEC, key_prefix="index_page")
@vary_on_cookie
def index(request):
    """Render index page of posts app."""
    title = "Последние обновления на сайте"
    template = "posts/index.html"
    posts_list = Post.objects.all()
    page_obj = make_pagination_obj(request, posts_list, MAX_POSTS_PER_PAGE)

    context = {
        "page_obj": page_obj,
        "title": title,
        "is_group_link": True,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Render group page of group app."""
    title = f"Записи сообщества {slug}"
    template = "posts/group_list.html"

    group = get_object_or_404(Group, slug=slug)
    posts_list = group.posts.all()
    page_obj = make_pagination_obj(request, posts_list, MAX_POSTS_PER_PAGE)

    context = {
        "title": title,
        "page_obj": page_obj,
        "group": group,
        "is_group_link": False,
    }
    return render(request, template, context)


def profile(request, username):
    """Render profile page."""
    title = f"Профайл пользователя {username}"
    template = "posts/profile.html"

    user_profile = get_object_or_404(User, username=username)
    posts_list = user_profile.posts.all()
    page_obj = make_pagination_obj(request, posts_list, MAX_POSTS_PER_PAGE)
    if request.user.is_authenticated and request.user != user_profile:
        is_following = (
            Follow.objects.filter(author=user_profile)
            .filter(user=request.user)
            .exists()
        )
        is_not_self = True
    else:
        is_following = False
        is_not_self = False

    context = {
        "title": title,
        "page_obj": page_obj,
        "user_profile": user_profile,
        "is_group_link": True,
        "following": is_following,
        "is_not_self": is_not_self,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Render post detail page."""
    template = "posts/post_detail.html"

    post = get_object_or_404(Post, pk=post_id)
    comment_list = post.comments.all()
    page_obj = make_pagination_obj(
        request, comment_list, MAX_COMMENTS_PER_PAGE,
    )

    is_author = post.author == request.user
    form = CommentForm()

    context = {
        "post": post,
        "is_author": is_author,
        "form": form,
        "page_obj": page_obj,
        "comments": comment_list,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Process posts creation."""
    if request.method != "POST":
        form = PostForm()
        return render(request, "posts/post_create.html", {"form": form})
    form = PostForm(
        request.POST,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, "posts/post_create.html", {"form": form})
    instance = form.save(commit=False)
    instance.author = request.user
    instance.save()

    return redirect(
        reverse_lazy(
            "posts:profile",
            kwargs={"username": request.user.username},
        ),
    )


@login_required
def post_edit(request, post_id=None):
    """Process posts edition."""
    instance = get_object_or_404(Post, pk=post_id)
    if instance.author != request.user:
        return redirect(
            reverse_lazy(
                "posts:post_detail",
                kwargs={"post_id": post_id},
            ),
        )
    if request.method == "POST":
        form = PostForm(
            request.POST, files=request.FILES or None, instance=instance,
        )
        if not form.is_valid():
            return render(request, "posts/post_create.html", {"form": form})
        instance.save()

        return redirect(
            reverse_lazy("posts:post_detail", kwargs={"post_id": post_id}),
        )
    form = PostForm(instance=instance)
    is_edit = True

    context = {
        "form": form,
        "is_edit": is_edit,
    }
    return render(request, "posts/post_create.html", context)


@login_required
def add_comment(request, post_id=None):
    """Process comment creation."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    """Render following list."""
    title = "Последние обновления в подписках"
    template = "posts/follow.html"

    posts_list = Post.objects.filter(author__following__user=request.user)
    page_obj = make_pagination_obj(request, posts_list, MAX_POSTS_PER_PAGE)

    context = {
        "page_obj": page_obj,
        "title": title,
        "is_group_link": True,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Process following."""
    following_profile = get_object_or_404(User, username=username)
    if following_profile == request.user:
        return redirect(
            reverse_lazy("posts:profile", kwargs={"username": username}),
        )
    Follow.objects.get_or_create(
        user=request.user,
        author=following_profile,
    )

    return redirect(
        reverse_lazy("posts:profile", kwargs={"username": username}),
    )


@login_required
def profile_unfollow(request, username):
    """Process unfollowing."""
    following_profile = get_object_or_404(User, username=username)
    if following_profile == request.user:
        return redirect(
            reverse_lazy("posts:profile", kwargs={"username": username}),
        )
    follower = Follow.objects.filter(author=following_profile)
    if follower.exists():
        follower.delete()

    return redirect(
        reverse_lazy("posts:profile", kwargs={"username": username}),
    )
