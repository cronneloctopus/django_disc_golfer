from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^$',
        'score_keeper.views.Index',
        name='index'
    ),
    url(
        r'^course/(?P<slug>[-\w]+)/$',
        'score_keeper.views.CourseDetail',
        name='course_detail'
    ),
)
