import django_tables2 as tables
from .models import Video
from django_tables2.utils import A


class VideoTable(tables.Table):
    # title = tables.Column(
    #     linkify=lambda record: record.url, verbose_name="Cím (kattintható)"
    # )

    # url = tables.URLColumn(
    #     verbose_name="YouTube link", accessor="url", attrs={"a": {"target": "_blank"}}
    # )
    title = tables.Column(
        linkify=lambda record: record.url,
        verbose_name="Cím (kattintható)"
    )
    class Meta:
        model = Video
        template_name = "django_tables2/bootstrap5.html"  # ezt a template használja a bootstrap 5-öt
        # https://django-tables2.readthedocs.io/en/latest/pages/custom-rendering.html
        fields = ("title", "category", "description")
