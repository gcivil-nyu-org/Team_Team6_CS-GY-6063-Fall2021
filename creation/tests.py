from django.test import TestCase

# Create your tests here.
# I want to test the views of creation app

creation_url = "/creation/"


class CreationTest(TestCase):
    def test_creation_page_url(self):
        response = self.client.get(creation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "creation/index.html")

    # def test_creation_search(self):
    #     self.client.post(
    #         creation_url,
    #         data={
    #             "user_input_term": "barbecue",
    #             "user_input_location": "100willoughby",
    #         },
    #         follow=True,
    #     )
