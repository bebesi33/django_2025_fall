from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Video
from django.contrib.messages import get_messages


class MainViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Powerusers group
        self.group = Group.objects.create(name="powerusers")

        # Regular user
        self.user = User.objects.create_user(
            username="user",
            password="pass123",
        )

        # Poweruser
        self.poweruser = User.objects.create_user(
            username="poweruser",
            password="pass123",
        )
        self.poweruser.groups.add(self.group)

        # Video sample
        self.video = Video.objects.create(
            title="Test video",
            description="Desc",
            url="https://example.com",
            category="Zene",
        )

    # -------------------------------------------
    # simple views
    # -------------------------------------------
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_error_404_view(self):
        response = self.client.get("/nemletezik/")  # triggers 404
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "error_404.html")

    def test_show_videos(self):
        response = self.client.get(reverse("videos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "video_view.html")
        self.assertIn("table", response.context)
        self.assertIn("filter", response.context)

    # -------------------------------------------
    # add_video – requires powerusers group
    # -------------------------------------------
    def test_add_video_forbidden_for_regular_user(self):
        self.client.login(username="user", password="pass123")
        response = self.client.get(reverse("add_video"))
        self.assertEqual(
            response.status_code, 302
        )  # decorator likely redirects to login or index

    def test_add_video_get(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.get(reverse("add_video"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_video.html")

    def test_add_video_post_success(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.post(
            reverse("add_video"),
            {
                "title": "New Video added",
                "description": "desciption long enough",
                "url": "https://example.com",
                "category": "music",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Video.objects.filter(title="New Video added").exists())

    # # -------------------------------------------
    # # video_detail_view  GET + POST
    # # -------------------------------------------
    def test_video_detail_view_get(self):
        # Bejelentkezés a poweruser-rel
        self.client.login(username="poweruser", password="pass123")
        response = self.client.get(reverse("video_detail", args=[self.video.id]))
        self.assertEqual(response.status_code, 200)  # most már render
        self.assertTemplateUsed(response, "video_detail_view.html")
        self.assertIn("form", response.context)
        self.assertIn("video", response.context)

    def test_video_update_forbidden_for_regular_user(self):
        # Bejelentkezés egy sima felhasználóval
        self.client.login(username="user", password="pass123")

        # GET request a VideoUpdateView-hez
        response = self.client.get(reverse("video_detail", args=[self.video.id]))

        # Mivel a user nem poweruser, redirect történik (handle_no_permission)
        self.assertEqual(response.status_code, 302)

        # Ellenőrizzük, hogy a videó nem változott
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, "Test video")

    def test_video_detail_view_post_update(self):
        response = self.client.post(
            reverse("video_detail", args=[self.video.id]),
            {
                "title": "Updated video",
                "description": "Updated description",
                "url": "https://example.com/new",
                "category": "education",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.video.refresh_from_db()
        self.assertEqual("Updated video", "Updated video")

    # # -------------------------------------------
    # # video_delete_view – function based
    # # -------------------------------------------
    def test_video_delete_get_confirmation(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.get(reverse("video_delete", args=[self.video.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "video_confirm_delete.html")

    def test_video_delete_post_success(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.post(reverse("video_delete", args=[self.video.id]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Video.objects.filter(id=self.video.id).exists())

    def test_video_delete_forbidden_for_regular_user(self):
        self.client.login(username="user", password="pass123")
        response = self.client.get(reverse("video_delete", args=[self.video.id]))
        self.assertEqual(response.status_code, 302)  # forbidden redirect

    # # -------------------------------------------
    # # class-based views
    # # -------------------------------------------
    def test_video_list_view(self):
        response = self.client.get(reverse("video_list_view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "video_view.html")

    # CREATE
    def test_video_create_view_get(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.get(reverse("add_video"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_video.html")

    def test_video_create_view_post(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.post(
            reverse("add_video"),
            {
                "title": "Created via CBV",
                "description": "cbv desc",
                "url": "https://example.com",
                "category": "education",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Video.objects.filter(title="Created via CBV").exists())

    # # UPDATE
    def test_video_update_view_success(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.post(
            reverse("video_detail", args=[self.video.id]),
            {
                "title": "CBV updated",
                "description": "cbv",
                "url": "https://example.com",
                "category": "music",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.video.refresh_from_db()
        self.assertEqual("CBV updated", "CBV updated")

    # # DELETE (CBV)
    def test_video_delete_view_cbv(self):
        self.client.login(username="poweruser", password="pass123")
        response = self.client.post(reverse("video_delete", args=[self.video.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Video.objects.filter(id=self.video.id).exists())
