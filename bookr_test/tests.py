from django.test import TestCase, Client
from .models import Publisher
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class TestPublisherModel(TestCase):
    """Test the publisher model."""
    def setUp(self):
        self.p = Publisher(name='Packt', \
        website='www.packt.com', \
        email='contact@packt.com')

    def test_create_publisher(self):
        #checks if the model object belongs to the Publisher instance
        self.assertIsInstance(self.p, Publisher)

    def test_str_representation(self):
        #checks if the string representation is as expected from the model definition
        self.assertEquals(str(self.p), "Packt")

class TestGreetingView(TestCase):
    """Test the greeting view."""
    def setUp(self):
        self.client = Client()

    def test_greeting_view(self):
        url = reverse('greeting_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestLoggedInGreetingView(TestCase):
    def setUp(self):
        # 1. No need to save manually
        self.user = User.objects.create_user(
            username='testuser',
            password='test@#628password'
        )
        # 2. self.client is already available via TestCase

    def test_user_greeting_not_authenticated(self):
        # 3. Use reverse instead of hardcoded strings
        # This reverse function maps to the name variable in the path of in urls.py
        url = reverse('greeting_view_user')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_user_authenticated(self):
        # 4. Login using the credentials created in setUp
        self.client.login(username='testuser', password='test@#628password')

        # This reverse function maps to the name variable in the path of in urls.py
        url = reverse('greeting_view_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



# redundant code
# class TestLoggedInGreetingView(TestCase):
#     """Test the greeting view for the authenticated users."""
#     def setUp(self):
#         test_user = User.objects.create_user\
#         (username='testuser', \
#         password='test@#628password')
#         test_user.save()
#         self.client = Client()
#
#     def test_user_greeting_not_authenticated(self):
#         response = self.client.get('/test/greet_user')
#         self.assertEquals(response.status_code, 302)
#
#     def test_user_authenticated(self):
#         login = self.client.login\
#         (username='testuser', \
#         password='test@#628password')
#         response = self.client.get('/test/greet_user')
#         self.assertEquals(response.status_code, 200)
#
