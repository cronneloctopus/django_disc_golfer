from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Model for disc golf course detail.
    """
    name = models.CharField(max_length=255)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=455)
    par = models.IntegerField(max_length=255, blank=True, null=True)
    #TODO: thumbnail = db.ImageField()

    def __unicode__(self):
        return self.name


class ScoreCard(models.Model):
    """
    Model for user scores by course.
    """
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    baskets = models.IntegerField()
    handicap = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s | %s | %s (%s)" % (
            self.user, self.course, self.score, self.baskets
        )
