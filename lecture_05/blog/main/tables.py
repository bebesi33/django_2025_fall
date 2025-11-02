import django_tables2 as tables
from .models import BlogPost
from django_tables2.utils import A


class BlogPostTable(tables.Table):
    # id = tables.LinkColumn("post_detail", args=[A("title")],  verbose_name='Post Title')
    class Meta:
        model = BlogPost
        template_name = "django_tables2/bootstrap5.html"  # ezt a template használja a bootstrap 5-öt
        # https://django-tables2.readthedocs.io/en/latest/pages/custom-rendering.html
        fields = ("title", "content")
