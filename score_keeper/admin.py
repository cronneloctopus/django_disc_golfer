from django.contrib import admin
from score_keeper.models import Course


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


# --- register models with Admin --- #
admin.site.register(Course, CourseAdmin)
