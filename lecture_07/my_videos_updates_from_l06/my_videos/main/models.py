from django.db import models


class Video(models.Model):
    CATEGORY_CHOICES = [
        ("education", "Oktatás"),
        ("music", "Zene"),
        ("entertainment", "Szórakozás"),
        ("tech", "Technológia"),
        ("other", "Egyéb"),
    ]

    title = models.CharField(max_length=200, verbose_name="Cím", help_text="A videó címe")
    url = models.URLField(verbose_name="Video link", help_text="A videó URL címe")
    description = models.TextField(blank=True, verbose_name="Leírás", help_text="A videó leírása")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="other",
        verbose_name="Kategória",
        help_text="A videó kategóriája",
    )

    def __str__(self):
        return f"{self.title} ({self.category})"

    class Meta:
        ordering = ["title"]
        verbose_name = "videó lista"
        verbose_name_plural = "Videók"
