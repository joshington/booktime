from decimal import Decimal
from django.test import TestCase
from main import models
#nCreate your tests here
from io import StringIO
import tempfile
from django.conf import settings
from django.core.management import call_command 
from django.test import TestCase, override_settings

from django.urls import reverse

from unittest.mock import patch
from django.contrib import auth
from main import forms

#==we want to make sure that 
class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')
    
    def test_about_us_page_works(self):
        response = self.client.get("/about-us/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'BookTime')


    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(
            response.context["form"], forms.UserCreationForm
        )
    
    def test_user_signup_page_submission_works(self):
        post_data = {
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }

        with patch.object(
            forms.UserCreationForm, "send_mail"
        ) as mock_send:
            response =self.client.post(reverse("signup"), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            models.User.objects.filter(
                email="user@domain.com"
            ).exists()
        ) 
        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )
        mock_send.assert_called_once()
        #using the mock module to test that the end_mail() function was called

#testing that our Product  manager works
class TestModel(TestCase):
    def test_active_manager_works(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            price=Decimal("10.00"))
        models.Product.objects.create(
            name="Pride and Prejudice",
            price=Decimal("2.00"))
        models.Product.objects.create(
            name="A Tale of Two Cities",
            price=Decimal("2.00"),
            active=False)
        self.assertEqual(len(models.Product.objects.active()), 2)

#testing the commands in the command.py
#decorator override_settings is used to override django settings for a specific test
#we are creating a new temporary folder as MEDIA_ROOT because we are dealing with potentially
#many uploaded files, django unlike the db, does not clean these files, using a temp folder
#makes sure this will be eventually cleaned by the OS.
#====exercise our test doesot test for the csv file to exist, images to be present in the basedir
#and so on, so its an exercise
class TestImport(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_import_data(self):
        out = StringIO()
        args = ['main/fixtures/product-sample.csv', 'main/fixtures/product-sampleimages/']
        call_command('import_data', *args, stdout=out)
        expected_out = (
                            "Importing products\n"
                            "Products processed=3 (created=3)\n"
                            "Tags processed=6 (created=6)\n"
                            "Images processed=3\n"
                        )
        self.assertEqual(out.getvalue(), expected_out)
        self.assertEqual(models.Product.objects.count(), 3)
        self.assertEqual(models.ProductTag.objects.count(), 6)
        self.assertEqual(models.ProductImage.objects.count(), 3)

#adding tests for the product list view
class TestPage(TestCase):
    def test_products_page_returns_active(self):
        models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        models.Product.objects.create(
            name="A Tale of Two Cities",
            slug="tale-two-cities",
            price=Decimal("2.00"),
            active=False,
        )
        response = self.client.get(
            reverse("products", kwargs={"tag": "all"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")
        product_list = models.Product.objects.active().order_by(
            "name"
        )
        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )

    def test_products_page_filters_by_tags_and_active(self):
        cb = models.Product.objects.create(
            name="The cathedral and the bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.00"),
        )
        cb.tags.create(name="Open source", slug="opensource")
        models.Product.objects.create(
            name="Microsoft Windows guide",
            slug="microsoft-windows-guide",
            price=Decimal("12.00"),
        )
        response = self.client.get(
            reverse("products", kwargs={"tag": "opensource"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BookTime")
        product_list = (
            models.Product.objects.active()
            .filter(tags__slug="opensource")
            .order_by("name")
        )
        self.assertEqual(
            list(response.context["object_list"]),
            list(product_list),
        )