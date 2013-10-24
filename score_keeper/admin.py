from django.contrib import admin
from score_keeper.models import Course, ScoreCard


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class ScoreCardAdmin(admin.ModelAdmin):
    pass


# --- register models with Admin --- #
admin.site.register(Course, CourseAdmin)
admin.site.register(ScoreCard, ScoreCardAdmin)
