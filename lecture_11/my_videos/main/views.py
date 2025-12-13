from django.shortcuts import get_object_or_404, redirect, render
import logging

from django.urls import reverse_lazy
from django_tables2 import RequestConfig, SingleTableMixin

from main.filters import VideoFilter
from main.forms import VideoForm
from main.models import Video
from main.tables import VideoTable
from django.views.generic import ListView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from users.perm_decorators import group_required, group_required_django
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


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
    video_filter = VideoFilter(request.GET, queryset=queryset)
    video_table = VideoTable(video_filter.qs)
    RequestConfig(request, paginate={"per_page": 5}).configure(video_table)
    # erre itt találtok példákat: https://django-tables2.readthedocs.io/en/latest/pages/pagination.html
    return render(
        request, "video_view.html", {"table": video_table, "filter": video_filter}
    )


@group_required_django("powerusers")
def add_video(request):
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("videos")
    else:
        form = VideoForm()
    return render(request, "add_video.html", {"form": form})


def video_detail_view(request, id):
    video = get_object_or_404(Video, pk=id)
    # Na ez a rész gondoskodik róla, hogy mindig vagy egy létező videót kapjunk,
    # vagy egy korrekt hibát lássunk. Nincs szükség try-except-re, mert a get_object_or_404 elintézi.
    # Get esetben nyilván üres lesz
    if request.method == "POST":
        form = VideoForm(request.POST, instance=video)
        # Az instance=video azt jelenti, hogy a form az adott videóhoz tartozik
        # — tehát nem új objektumot hoz létre, hanem egy meglévőt szerkeszt.
        # Az űrlap elküldése esetén frissítjük a videó adatait
        # ez a művelet egy post request...
        form = VideoForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect("videos")
    else:
        form = VideoForm(instance=video)
        # Ilyenkor csak betölti az adott videó adatait az űrlapba, de nem ment semmit.
        # ez a get művelet esete (amikor kattintunk az oldalra)
    return render(request, "video_detail_view.html", {"video": video, "form": form})


# def video_delete_view(request, id):
#     """Rövid , nem túl korrekt verzió"""
#     video = get_object_or_404(Video, pk=id)
#     if request.method == "POST":
#         video.delete()
#     return redirect("videos")


@group_required("powerusers")
def video_delete_view(request, id):
    video = get_object_or_404(Video, pk=id)

    if request.method == "POST":
        video.delete()
        return redirect("videos")

    # Ha GET kérés érkezik, mutassunk egy megerősítő oldalt
    return render(request, "video_confirm_delete.html", {"video": video})


#################################
####### Class based view ########
#################################

# Naív megoldás....
# class VideoListView(ListView):
#     model = Video
#     paginate_by = 3
#     template_name = "video_class_list_view.html"  # the associated template's name
#     context_object_name = (
#         "videos"  # for convinience, this is the name of the object in the template
#     )


class VideoListView(SingleTableMixin, FilterView):
    model = Video
    table_class = VideoTable
    template_name = "video_view.html"
    filterset_class = VideoFilter
    paginate_by = 5


@method_decorator(group_required("powerusers"), name="dispatch")
class VideoCreateView(CreateView):
    model = Video
    form_class = VideoForm
    template_name = "add_video.html"
    success_url = reverse_lazy("videos")  # redirect sikeres mentés után
    # a reverse_lazy() nem azonnal, hanem csak akkor fut le, amikor ténylegesen szükség van az URL-re
    # — például amikor a view sikeresen menti az objektumot, és tényleg redirect-elni kell.


class UserPassesSuperUserTest(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="powerusers").exists()

    def handle_no_permission(self):
        messages.warning(
            self.request, "Nincs jogosultságod ehhez az oldalhoz.", extra_tags="login"
        )
        return redirect("index")


class VideoUpdateView(UserPassesSuperUserTest, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = "video_detail_view.html"  # ugyanaz a sablon
    pk_url_kwarg = "id"  # a url-ből veszi az id-t
    success_url = reverse_lazy("videos")  # hová redirectel mentés után


@method_decorator(group_required("powerusers"), name="dispatch")
class VideoDeleteView(DeleteView):
    model = Video
    template_name = "video_confirm_delete.html"  # sablon a törlés megerősítéséhez
    pk_url_kwarg = "id"  # az URL-ből veszi az id-t
    success_url = reverse_lazy("videos")
