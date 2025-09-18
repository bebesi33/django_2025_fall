from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "name": "László Bebesi"
    }
    return render(request, "index.html", context)


def error_404_view(request, exception):
    return render(request, 'e404.html', status=404)
