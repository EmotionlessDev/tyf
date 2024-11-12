from django.contrib import admin
from .models import University, Major


class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "city")

    list_filter = ("name", "country", "city")

    search_fields = ("name", "country", "city")


class MajorAdmin(admin.ModelAdmin):
    list_display = ("name", "code")

    list_filter = ("name",)

    search_fields = ("name",)


admin.site.register(University, UniversityAdmin)
admin.site.register(Major, MajorAdmin)
