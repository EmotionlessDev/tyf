from .models import Post, Comment
from django.http import HttpResponse, HttpRequest
from users.models import User
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from users.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.apps import apps
from django.views.generic import DetailView

# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     comments = post.comments.filter(active=True, parent__isnull=True)
#     if request.method == "POST":
#         # comment has been added
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             parent_obj = None
#             # get parent comment id from hidden input
#             try:
#                 # id integer e.g. 15
#                 parent_id = int(request.POST.get("parent_id"))
#             except:
#                 parent_id = None
#             # if parent_id has been submitted get parent_obj id
#             if parent_id:
#                 parent_obj = Comment.objects.get(id=parent_id)
#                 # if parent object exist
#                 if parent_obj:
#                     # create replay comment object
#                     replay_comment = comment_form.save(commit=False)
#                     # assign parent_obj to replay comment
#                     replay_comment.parent = parent_obj
#             # normal comment
#             # create comment object but do not save to database
#             new_comment = comment_form.save(commit=False)
#             # assign ship to the comment
#             new_comment.post = post
#             # save
#             new_comment.save()
#             return HttpResponseRedirect(post.get_absolute_url())
#     else:
#         comment_form = CommentForm()
#     return render(
#         request,
#         "core/detail.html",
#         {"post": post, "comments": comments, "comment_form": comment_form},
#     )

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("#")
        else:
            if "email" in form.errors.keys():
                messages.error(request, form.errors["email"][0])
            elif "password1" in form.errors.keys():
                messages.error(request, form.errors["password1"][0])
            elif "password2" in form.errors.keys():
                messages.error(request, form.errors["password2"][0])
            print(form.errors.as_text())

    context = {"form": form}
    return render(request, "main/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email")
            return HttpResponseRedirect("")

        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return HttpResponseRedirect("")
        else:
            login_user(request, user)
            return HttpResponseRedirect("/")

    return render(request, "main/login.html")


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/login/")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "main/blank.html", {"user": request.user})


def profile(request: HttpRequest, username: str) -> HttpResponse:
    user_posts = Post.objects.filter(author__username=username)
    user = get_object_or_404(User, username=username)
    return render(request, "main/profile.html", {"user": user, "posts": user_posts})


def single_post(request: HttpRequest) -> HttpResponse:
    return render(request, "main/single-post.html")


class PostDetailView(DetailView):
    model = Post
    template_name = 'main/single-post.html'
    context_object_name = 'post'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
