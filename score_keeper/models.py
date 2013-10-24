from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Avg, Max, Min

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
    created = models.DateTimeField()
    score = models.IntegerField()
    baskets = models.IntegerField(
        choices=BASKETS_CHOICE, default=9
    )
    handicap = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s | %s | %s (%s)" % (
            self.user, self.course, self.score, self.baskets
        )

    def get_scores_by_round(user, course):
        all_scores = ScoreCard.get_scores_by_round(
            user=user, course=course
        )
        if all_scores:
            nine_scores = all_scores.filter(baskets=9).aggregate(
                Avg('score'), Max('score'), Min('score')
            )
            eighteen_scores = all_scores.filter(baskets=18).aggregate(
                Avg('score'), Max('score'), Min('score')
            )
        return nine_scores, eighteen_scores


        """
        if all_scores:
            # get data of last round
            data['last_round'] = all_scores[0]

            for card in all_scores:
                if card.baskets == 9 and card.score:
                    nine_count += 1
                    nine_scores.append((card.created, card.score))
                    data['nine_sum'] += card.score
                elif card.baskets == 18 and card.score:
                    eighteen_count += 1
                    eighteen_scores.append((card.created, card.score))
                    data['eighteen_sum'] += card.score

            data['nine_scores'] = nine_scores
            data['eighteen_scores'] = eighteen_scores

            # get avgs
            if data['nine_sum']:
                data['nine_avg'] = data['nine_sum'] / len(nine_scores)
            if data['eighteen_sum']:
                data['eighteen_avg'] = data['eighteen_sum'] / len(eighteen_scores)

            # get min, max
            if len(nine_scores) > 0:
                data['nine_max'] = map(max, zip(*nine_scores))
                data['nine_min'] = map(min, zip(*nine_scores))
            if len(eighteen_scores) > 0:
                data['eighteen_max'] = map(max, zip(*eighteen_scores))
                data['eighteen_min'] = map(min, zip(*eighteen_scores))
        """

        return data
