from django.shortcuts import render
import logging

from django_tables2 import RequestConfig

from main.filters import VideoFilter
from main.models import Video
from main.tables import VideoTable

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    index_context = dict()
    return render(request, "index.html", index_context)


def error_404_view(request, exception):
    logger.error(f"Hibák vannak és lesznek: {exception}")
    return render(request, "error_404.html", status=404)


def show_videos(request):
    queryset = Video.objects.all()
    blog_filter = VideoFilter(request.GET, queryset=queryset)
    blog_table = VideoTable(blog_filter.qs)
    RequestConfig(request, paginate={"per_page": 5}).configure(blog_table)
    # erre itt találtok példákat: https://django-tables2.readthedocs.io/en/latest/pages/pagination.html
    return render(request, "video_view.html", {"table": blog_table, "filter": blog_filter})
