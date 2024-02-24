from django.test import TestCase
from base.models import Profile

# Create your tests here.
class NippoTestCase(TestCase):
    def setUp(self):
        obj = Profile(name="test", zipcode=123)
        obj.save()
    
    def test_saved_single_object(self):
        count = Profile.objects.count()
        self.assertEqual(count, 1)