from django.test import TestCase
from resources.venues.models import Venue
# Create your tests here.
# I want to test the views of creation app

creation_url = "/creation/"

class CreationTest(TestCase):
    def setUp(self):
        self.term = "barbecue"
        self.location = "100 willoughby"

    def test_creation_page_url(self):
        response = self.client.get(creation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "creation/index.html")

    def test_creation_search(self):
        response = self.client.post(
            creation_url,
            data={
                "user_input_term":self.term,
                "user_input_location":self.location,
            },
        )
        self.assertEqual(response.status_code,200)


