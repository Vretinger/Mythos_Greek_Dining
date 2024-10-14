# tests.py
from django.test import TestCase
from django.urls import reverse
from .forms import ContactForm
from .models import ContactMessage
from django.contrib.messages import get_messages


class ContactFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        form_data = {
            'name': '',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class ContactViewTest(TestCase):

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact.html')

    def test_contact_view_post_valid(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertTrue(any(msg.message == 'Your message has been sent successfully!' for msg in get_messages(response.wsgi_request)))

    def test_contact_view_post_invalid(self):
        response = self.client.post(reverse('contact'), {
            'name': '',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)  # Should return to the form
        self.assertEqual(ContactMessage.objects.count(), 0)  # No message saved
