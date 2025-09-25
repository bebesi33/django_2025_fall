from django.shortcuts import render
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def index(request):
    index_context = dict()
    index_context["name"] = "Bebesi Laszlo"
    index_context["neptun"] = "DFFKZ4"
    index_context["now2"] = datetime.now
    logger.warning(datetime.now())
    return render(request, "index.html", index_context)


def contact(request):
    return render(request, "contact.html")


def schedule(request):
    return render(request, "schedule.html")


def error_404_view(request, exception):
    logger.error(f"Hibák vannak és lesznek: {exception}")
    return render(request, "error_404.html", status=404)
