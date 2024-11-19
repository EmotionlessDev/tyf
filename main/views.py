import json
import markdown
from users.utils import (
    OTPTools,
    sendEmail,
    EncryptTools,
    AccountActivationToken,
)
from django.apps import apps
from user_agents import parse
from users.models import User
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.views.generic import DetailView
from social_django.models import UserSocialAuth
from django.utils.encoding import force_bytes, force_str
from users.forms import UserCreationForm, UserSetPasswordForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.http import (
    Http404,
    JsonResponse,
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
)
from .models import Profile, Follow, Collection, Category, Tag, Media, Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm, EditProfileForm
from django.utils import timezone
from django.db import transaction


def index(request: HttpRequest) -> HttpResponse:
    collections = Collection.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        "user": request.user,
        "collections": collections,
        "categories": categories,
        "tags": tags,
    }

    return render(request, "main/index.html", context=context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    profile = get_object_or_404(Profile, username=username)

    def get_is_following_or_none(profile):
        if not request.user.is_authenticated:
            return None
        return request.user.profile.is_following(profile)

    followings = [
        (x.following, get_is_following_or_none(x.following))
        for x in profile.following.all()
    ]
    followers = [
        (x.follower, get_is_following_or_none(x.follower))
        for x in profile.followers.all()
    ]

    is_following = get_is_following_or_none(profile)

    context = {
        "profile": profile,
        "followings": followings,
        "followers": followers,
        "is_following": is_following,
    }

    return render(request, "main/profile.html", context)


def login(request):
    email = ""

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        if UserSocialAuth.objects.filter(user__email=email).exists():
            messages.info(
                request,
                "User with this Email was registered using Google/Yandex. Please sign in using same method.",
            )
            return render(request, "main/login.html", {"email": email})

        if not User.objects.filter(email=email).exists():
            messages.error(request, "User with this Email doesn't exists.")
            return render(request, "main/login.html", {"email": email})
        else:
            if not User.objects.get(email=email).is_active:
                messages.info(
                    request,
                    "This user has not verified Email. Please Sign Up again.",
                )
                return render(request, "main/login.html", {"email": email})

        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request, "Incorrect Password.")
            return render(request, "main/login.html", {"email": email})
        else:
            login_user(request, user)

            if user.is_superuser:
                return redirect(reverse("admin:index"))
            return redirect("/")

    return render(request, "main/login.html", {"email": email})


def register(request):
    email = ""

    if request.method == "POST":
        email = request.POST["email"].lower()
        if UserSocialAuth.objects.filter(user__email=email).exists():
            messages.info(
                request,
                "User with this Email was registered using Google/Yandex. Please sign in using same method.",
            )
            return render(request, "main/register.html", {"email": email})

        if User.objects.filter(email=email).exists():
            if not User.objects.get(email=email).is_active:
                user = User.objects.get(email=email)
                user.delete()

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            otp = OTPTools.generateOTP()
            url_token = EncryptTools.generateToken(
                remote_addr=request.META["REMOTE_ADDR"],
                local_username=request.META["USER"],
                device_name=parse(request.META["HTTP_USER_AGENT"]).device.model,
            )
            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=EncryptTools.getHash(url_token)
            )
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            cache.set(
                key=redis_key,
                value={
                    "otp": EncryptTools.getHash(otp["otp"]),
                    "otp_ttl": otp["ttl"],
                    "is_register_confirm": True,
                    "is_reset_password_confirm": False,
                    "user_token": AccountActivationToken.make_token(user=user),
                },
                timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
            )

            sendEmail(user=user, otp=otp["otp"], register_cofirm=True)

            return redirect(
                reverse("verification", kwargs={"token": url_token, "uidb64": uid})
            )
        else:
            if "email" in form.errors.keys():
                messages.error(request, form.errors["email"][0])
            elif "password1" in form.errors.keys():
                messages.error(request, form.errors["password1"][0])
            elif "password2" in form.errors.keys():
                messages.error(request, form.errors["password2"][0])

    return render(request, "main/register.html", {"email": email})


def logout(request):
    logout_user(request)
    return redirect("/login/")


def resetPassword(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()

        if not User.objects.filter(email=email).exists():
            messages.error(request, "User with this Email does't exists.")
            return redirect("/login/reset_password/")

        user = User.objects.get(email=email)

        otp = OTPTools.generateOTP()
        url_token = EncryptTools.generateToken(
            remote_addr=request.META["REMOTE_ADDR"],
            local_username=request.META["USER"],
            device_name=parse(request.META["HTTP_USER_AGENT"]).device.model,
        )
        redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
            token=EncryptTools.getHash(url_token)
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        cache.set(
            key=redis_key,
            value={
                "otp": EncryptTools.getHash(otp["otp"]),
                "otp_ttl": otp["ttl"],
                "is_register_confirm": False,
                "is_reset_password_confirm": True,
                "user_token": AccountActivationToken.make_token(user=user),
            },
            timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
        )

        sendEmail(user=user, otp=otp["otp"], reset_password=True)

        return redirect(
            reverse("verification", kwargs={"token": url_token, "uidb64": uid})
        )

    return render(request, "main/reset_password.html")


def setPassword(request, uidb64, token):
    if (
        EncryptTools.generateToken(
            remote_addr=request.META["REMOTE_ADDR"],
            local_username=request.META["USER"],
            device_name=parse(request.META["HTTP_USER_AGENT"]).device.model,
        )
        != token
    ):
        raise Http404

    redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
        token=EncryptTools.getHash(token)
    )

    if cache.get(redis_key) is None:
        raise Http404
    else:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            raise Http404

        redis_data = cache.get(redis_key)

        if not (
            user is not None
            and AccountActivationToken.check_token(user, redis_data["user_token"])
        ):
            raise Http404

        form = UserSetPasswordForm(user)

        if request.method == "POST":
            form = UserSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "You have successfully changed your password!"
                )
                cache.delete(redis_key)
                return redirect("/login/")
            else:
                if "new_password1" in form.errors.keys():
                    messages.error(request, form.errors["new_password1"][0])
                elif "new_password2" in form.errors.keys():
                    messages.error(request, form.errors["new_password2"][0])

    return render(request, "main/set_password.html", {"form": form})


def verification(request, uidb64, token):
    if (
        EncryptTools.generateToken(
            remote_addr=request.META["REMOTE_ADDR"],
            local_username=request.META["USER"],
            device_name=parse(request.META["HTTP_USER_AGENT"]).device.model,
        )
        != token
    ):
        raise Http404
    redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
        token=EncryptTools.getHash(token)
    )

    if cache.get(redis_key) is None:
        raise Http404
    else:
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
            redis_data = cache.get(redis_key)
        except:
            raise Http404

        if not (
            user is not None
            and AccountActivationToken.check_token(user, redis_data["user_token"])
        ):
            raise Http404

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            if request.POST == {}:
                if bool(json.loads(request.body)["send_status"]):
                    cache.delete(redis_key)
                    otp = OTPTools.generateOTP()

                    cache.set(
                        key=redis_key,
                        value={
                            "otp": EncryptTools.getHash(otp["otp"]),
                            "otp_ttl": otp["ttl"],
                            "is_register_confirm": redis_data["is_register_confirm"],
                            "is_reset_password_confirm": redis_data[
                                "is_reset_password_confirm"
                            ],
                            "user_token": redis_data["user_token"],
                        },
                        timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
                    )

                    sendEmail(
                        user=user,
                        otp=otp["otp"],
                        reset_password=redis_data["is_reset_password_confirm"],
                        register_cofirm=redis_data["is_register_confirm"],
                    )

                    return JsonResponse(
                        {
                            "message": "New code has just been sent to your email!",
                        }
                    )
            else:
                if redis_data["otp_ttl"] < OTPTools.getCurrentTime():
                    return JsonResponse(
                        {
                            "redirect": False,
                            "message": "Your code has expired. Please resend!",
                        }
                    )
                else:
                    otp = ""
                    for i in range(1, 7):
                        otp += request.POST.get(f"{i}")
                    if not OTPTools.verifyOTP(
                        EncryptTools.getHash(otp), redis_data["otp"]
                    ):
                        return JsonResponse(
                            {
                                "redirect": False,
                                "message": "Invalid verification code",
                            }
                        )

                if redis_data["is_register_confirm"]:
                    cache.delete(redis_key)

                    user.is_active = True
                    user.save()
                    messages.success(request, "You have successfully registered!")

                    return JsonResponse(
                        {
                            "redirect": True,
                            "message": "/login/",
                        }
                    )
                elif redis_data["is_reset_password_confirm"]:
                    cache.delete(redis_key)

                    url_token = EncryptTools.generateToken(
                        remote_addr=request.META["REMOTE_ADDR"],
                        local_username=request.META["USER"],
                        device_name=parse(request.META["HTTP_USER_AGENT"]).device.model,
                    )
                    redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                        token=EncryptTools.getHash(url_token)
                    )
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    cache.set(
                        key=redis_key,
                        value={
                            "user_token": AccountActivationToken.make_token(user=user),
                        },
                        timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
                    )

                    return JsonResponse(
                        {
                            "redirect": True,
                            "message": reverse(
                                "set_password",
                                kwargs={"token": url_token, "uidb64": uid},
                            ),
                        }
                    )

        return render(
            request, "main/verification.html", context={"user_email": user.email}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = "main/post_detail.html"
    context_object_name = "post"
    slug_field = "identifier"
    slug_url_kwarg = "identifier"


def error400(request, exception):
    return render(request, "main/error_400.html", status=400)


def error403(request, exception):
    return render(request, "main/error_403.html", status=403)


def error404(request, exception):
    return render(request, "main/error_404.html", status=404)


def error500(request, *args, **argv):
    return render(request, "main/error_500.html", status=500)


def error505(request, *args, **argv):
    return render(request, "main/error_505.html", status=505)


def post_new(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                post = form.save(commit=False)
                post.author = request.user.profile
                post.save()
                media_files = request.FILES.getlist("media_files")
                for file in media_files:
                    Media.objects.create(content_object=post, file=file)
            return redirect("post_detail", identifier=post.identifier)
    else:
        form = PostForm()
    return render(request, "main/post_add.html", {"form": form})


@login_required
def follow(request, username):
    next = request.GET.get("next", "/")
    following = get_object_or_404(Profile, username=username)
    follower = request.user.profile
    if not follower.following.filter(following_id=following.id).exists():
        Follow.objects.create(follower=follower, following=following)
    return redirect(next)


@login_required
def unfollow(request, username):
    next = request.GET.get("next", "/")
    following = get_object_or_404(Profile, username=username)
    follower = request.user.profile
    follower.following.filter(following_id=following.id).delete()
    return redirect(next)


@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = EditProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if profile_form.is_valid():
            profile_form.save()

            if request.FILES.get("avatar", None) != None:
                request.user.profile.avatar = request.FILES["avatar"]
                request.user.profile.save()

            return redirect(to="profile", username=request.user.profile.username)
    else:
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, "main/edit_profile.html", {"profile_form": profile_form})
