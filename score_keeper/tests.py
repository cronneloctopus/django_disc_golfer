from django.test import TestCase
from .models import Course


class ScoreKeeperTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            name='jerico_park',
            lat=float(49.267539),
            lon=float(-123.200316),
        )

    def test_can_create_course(self):
        self.assertEqual(self.course.name, 'jerico_park')

    def test_course_url(self):
        pass
