import django_filters
from .models import Video
from django import forms


class VideoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Cím",
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Cím keresése'}),
    )
    description = django_filters.CharFilter(
        field_name="description",
        lookup_expr="icontains",
        label="Leírás",
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Tartalom keresése'}),
    )

    class Meta:
        model = Video
        fields = {
            "title": ["exact"],
            # "content": ["icontains"],
        }


