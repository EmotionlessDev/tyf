from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline


from .models import Category, Collection, Tag, Post, Comment, Media, Profile, Follow


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "username",
        "email",
        "first_name",
        "last_name",
        "university",
        "date_of_birth",
        "date_joined",
    )

    list_filter = (
        "username",
        "email",
        "date_of_birth",
        "date_joined",
        "major",
    )

    fieldsets = [
        (None, {"fields": ["user", "username", "email", "avatar", "date_joined"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "middle_name",
                    "university",
                    "major",
                    "bio",
                    "date_of_birth",
                    "telegram",
                    "vkontakte",
                ]
            },
        ),
        ("Stats", {"fields": ["points", "awards"]}),
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "major",
    ]

    ordering = [
        "username",
    ]

    autocomplete_fields = ["university", "major"]

    class Meta:
        model = Profile


class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "follower",
        "following",
        "created_at",
    ]

    class Meta:
        model = Follow


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Category


class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Collection


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Tag


class MediaInline(GenericStackedInline):
    model = Media
    extra = 1
    fields = ["file", "description"]


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class MediaAdmin(admin.ModelAdmin):
    list_display = ["file", "description", "content_type", "object_id"]
    search_fields = ["caption", "description"]


class CommentAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, MediaInline]

    list_display = [
        "title",
        "author",
        "category",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "author",
        "category",
        "tags",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "content",
        "author",
        "category",
        "tags",
    ]

    ordering = [
        "created_at",
        "updated_at",
    ]

    class Meta:
        model = Post


admin.site.register(Follow, FollowAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
