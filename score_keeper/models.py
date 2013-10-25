from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone


BASKETS_CHOICE = (
    (9, 'Nine'),
    (18, 'Eighteen'),
)


class Course(models.Model):
    """
    Model for disc golf course detail.
    """
    name = models.CharField(max_length=255)
    lat = models.FloatField(default=None, blank=True, null=True)
    lon = models.FloatField(default=None, blank=True, null=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=455)
    par = models.IntegerField(
        max_length=255, default=27, blank=True, null=True
    )
    #TODO: thumbnail = db.ImageField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return settings.SITE_URL + 'course/' + self.slug


class ScoreCard(models.Model):
    """
    Model for user scores by course.
    """
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    created = models.DateTimeField(default=timezone.now())
    score = models.IntegerField()
    baskets = models.IntegerField(
        choices=BASKETS_CHOICE, default=9
    )
    handicap = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s | %s | %s (%s)" % (
            self.user, self.course, self.score, self.baskets
        )

    class Meta:
        ordering = ('-created',)


class UserProfile(User):

    class Meta:
        proxy = True

    def get_last_round(self, course=None):
        qs = self.scorecard_set.all()
        if course:
            qs = qs.filter(user=self, course=course)
        last_round = qs[0]
        return last_round

    def get_course_avg(self, course=None, baskets=None):
        qs = self.scorecard_set.all()
        if course:
            qs = qs.filter(course=course)
        if baskets:
            qs = qs.filter(baskets=baskets)
        if len(qs) > 0:
            sum_scores = qs.aggregate(Sum('score'))
            sum_baskets = qs.aggregate(Sum('baskets'))
            return sum_scores.get('score__sum') / \
                sum_baskets.get('baskets__sum')
        else:
            return None

    def get_scores(self, course=None, baskets=None):
        qs = self.scorecard_set \
            .values('created', 'score') \
            .order_by('score')
        if course:
            qs = qs.filter(course=course)
        if baskets:
            qs = qs.filter(baskets=baskets)
        ql = list(qs)
        nine_max = ql[-1]
        nine_min = ql[0]
        sum_scores = 0
        for x in ql:
            sum_scores += x.get('score')
        nine_avg = sum_scores / len(qs)
        return nine_max, nine_min, nine_avg
