from django.shortcuts import render
import logging
from datetime import datetime
from main.models import Friend

logger = logging.getLogger(__name__)


def index(request):
    index_context = dict()
    friends = Friend.objects.all()
    index_context["friends"] = friends
    return render(request, "index.html", index_context)


def schedule(request):
    return render(request, "schedule.html")


def error_404_view(request, exception):
    logger.error(f"Hibák vannak és lesznek: {exception}")
    return render(request, "error_404.html", status=404)
