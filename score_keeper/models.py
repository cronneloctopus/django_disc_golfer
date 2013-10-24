from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Avg, Min, Max
from django.conf import settings
from datetime import datetime
from django.utils.timezone import utc


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
    created = models.DateTimeField(
        default=datetime.utcnow().replace(tzinfo=utc)
    )
    score = models.IntegerField()
    baskets = models.IntegerField(
        choices=BASKETS_CHOICE, default=9
    )
    handicap = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s | %s | %s (%s)" % (
            self.user, self.course, self.score, self.baskets
        )


class UserProfile(User):

    class Meta:
        proxy = True

    def get_course_avg(self, course):
        sum_scores = ScoreCard.objects.filter(course=course).aggregate(
            Sum('score')
        )
        sum_baskets = ScoreCard.objects.filter(course=course).aggregate(
            Sum('baskets')
        )
        return sum_scores.get('score__sum') / sum_baskets.get('baskets__sum')

    def get_nine_stats(self, course):
        qs = list(
            ScoreCard.objects.values('created', 'score')
            .filter(baskets=9)
            .order_by('score')
        )
        nine_max = qs[-1]
        nine_min = qs[0]
        sum_scores = 0
        for x in qs:
            sum_scores += x.get('score')
        nine_avg = sum_scores / len(qs)
        return nine_max, nine_min, nine_avg
