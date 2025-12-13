from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class AuthViewsTest(TransactionTestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    # ------------------------------
    # sign_in tests
    # ------------------------------
    def test_sign_in_success(self):
        response = self.client.post(
            reverse("sign_in"),
            {
                "username": "testuser",
                "password": "testpass123",
            },
        )

        # Always redirects to "index"
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

        # User should be authenticated
        self.assertTrue("_auth_user_id" in self.client.session)

        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(msgs[0].message, "Successful login!")
        self.assertEqual(msgs[0].extra_tags, "login")

    def test_sign_in_wrong_password(self):
        response = self.client.post(
            reverse("sign_in"),
            {
                "username": "testuser",
                "password": "wrongpass",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

        # User should NOT be authenticated
        self.assertFalse("_auth_user_id" in self.client.session)

        msgs = list(get_messages(response.wsgi_request))
        self.assertIn("Invalid username or password", msgs[0].message)

    def test_sign_in_redirect_when_already_logged_in(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("sign_in"))

        self.assertEqual(response.status_code, 403)
        self.assertIn(
            "This is only for non authenticated users...", response.content.decode()
        )

    # ------------------------------
    # sign_out tests
    # ------------------------------
    def test_sign_out_success(self):
        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("sign_out"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))

        # User should be logged out
        self.assertFalse("_auth_user_id" in self.client.session)

        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(msgs[0].message, "You have been logged out.")

    def test_sign_out_requires_login(self):
        response = self.client.get(reverse("sign_out"))

        # login_required → redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url.lower())

    # ------------------------------
    # registration function-based view
    # ------------------------------
    def test_registration_get(self):
        response = self.client.get(reverse("registration"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")
        self.assertIn("form", response.context)

    def test_registration_post_success(self):
        response = self.client.post(
            reverse("registration"),
            {
                "username": "newuser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )

        # Successful signup stays on registration page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")

        self.assertTrue(User.objects.filter(username="newuser").exists())

        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(msgs[0].message, "Successful Sign up!")

    def test_registration_post_invalid(self):
        response = self.client.post(
            reverse("registration"),
            {
                "username": "newuser",
                "password1": "x",
                "password2": "y",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")
        self.assertIn("form", response.context)

        msgs = list(get_messages(response.wsgi_request))
        self.assertIn("Invalid form submission!", msgs[0].message)

    # ------------------------------
    # RegisterView (class-based view)
    # ------------------------------
    def test_register_view_get(self):
        response = self.client.get(reverse("registration"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")
        self.assertIn("form", response.context)

    def test_register_view_post_success(self):
        response = self.client.post(
            reverse("registration"),
            {
                "username": "cbv_user",
                "password1": "StrongPass123.!",
                "password2": "StrongPass123.!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="cbv_user").exists())

        msgs = list(get_messages(response.wsgi_request))
        self.assertEqual(msgs[0].message, "Successful Sign up!")

    def test_register_view_post_invalid(self):
        response = self.client.post(
            reverse("registration"),
            {
                "username": "cbv_user",
                "password1": "x",
                "password2": "y",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")
        self.assertIn("form", response.context)

        msgs = list(get_messages(response.wsgi_request))
        self.assertIn("Invalid form submission!", msgs[0].message)
