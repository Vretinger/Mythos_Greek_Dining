from django.test import TestCase, Client
from django.urls import reverse

class MenuTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu_url = reverse('menu')

    def test_menu_page_loads(self):
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, 200)  # Check for successful response
        self.assertTemplateUsed(response, 'menu.html')

    def test_menu_items_displayed(self):
        response = self.client.get(self.menu_url)
        # Check that the response contains specific menu items
        self.assertContains(response, 'TZATZIKI')
        self.assertContains(response, '$6.99')
        self.assertContains(response, 'MOUSSAKA')
        self.assertContains(response, '$14.99')
        self.assertContains(response, 'BAKLAVA')
        self.assertContains(response, '$5.99')
