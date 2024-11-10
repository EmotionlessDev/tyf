from django.shortcuts import render, get_object_or_404
from users.models import User
from .models import Post, Comment


def index(request):
    return render(request, "main/blank.html")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "main/profile.html", {"user": user})


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
