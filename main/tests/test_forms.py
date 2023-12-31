
from django.test import TestCase
from django.core import mail 
from main import forms 
from django import reverse


class TestForm(TestCase):
    def test_valid_contact_us_fom_sends_email(self):
        form = forms.ContactForm({
            'name':"Luke Skywalker",
            'message':"Hi there"
        })
        self.assertTrue(form.is_valid())
        with self.assertLogs('main.forms', level='INFO') as cm:
            form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site message')
        self.assertGreaterEqual(len(cm.output), 1)
    
    def test_invalid_contact_us_form(self):
        form = forms.ContactForm({
            'message':"Hi there"
        })
        self.assertFalse(form.is_valid())
    
    #test that the view is rendered when hitting the URL, and the page contains form

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,  'main/contact_form.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(
            response.context["form"], forms.ContactForm
        )
    
    def test_valid_signup_form_sends_email(self):
        form = forms.UserCreationForm(
            {
                "email": "user@domain.com",
                "password1": "abcabcabc",
                "password2": "abcabcabc",
            }
        )
        self.assertTrue(form.is_valid())
        with self.assertLogs("main.forms", level="INFO") as cm:form.send_mail()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, "Welcome to BookTime"
        )
        self.assertGreaterEqual(len(cm.output), 1)
