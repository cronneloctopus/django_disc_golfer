from django.test import TestCase
from .models import Course, ScoreCard, UserProfile
from django.contrib.auth.models import User


class ScoreKeeperTest(TestCase):
    def setUp(self):
        self.userprofile = UserProfile.objects.create(
            username='sam',
            email='foo@bar.com',
        )
        self.course = Course.objects.create(
            name='jerico_park',
            lat=float(49.267539),
            lon=float(-123.200316),
        )
        self.score_first = ScoreCard.objects.create(
            user=self.userprofile,
            course=self.course,
            score=27,
            baskets=9,
        )
        self.score_second = ScoreCard.objects.create(
            user=self.userprofile,
            course=self.course,
            score=58,
            baskets=18,
        )
        self.score_third = ScoreCard.objects.create(
            user=self.userprofile,
            course=self.course,
            score=62,
            baskets=18,
        )

    def test_course_created(self):
        self.assertEqual(self.course.name, 'jerico_park')

    def test_score_created(self):
        self.assertEqual(self.score_first.score, 27)
        self.assertEqual(self.score_first.course.name, 'jerico_park')
        self.assertEqual(self.score_second.score, 58)
        self.assertEqual(self.score_first.course.name, 'jerico_park')

    def test_get_course_avg(self):
        avg = self.userprofile.get_course_avg(
            course=self.course
        )
        self.assertEqual(avg, 3)

    def test_get_nine_stats(self):
        nine_max, nine_min, nine_avg = self.userprofile.get_nine_stats(
            course=self.course
        )
        self.assertEqual(nine_max.get('score'), 27)
        self.assertEqual(nine_min.get('score'), 27)
        self.assertEqual(nine_avg, 27)

    def test_course_url(self):
        pass
