import django_filters
from .models import BlogPost
from django import forms


class BlogPostFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(
        field_name="content",
        lookup_expr="icontains",
        label="Tartalom",
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Cím keresése'}),
    )
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="exact",
        label="Cím",
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Tartalom keresése'}),
    )

    # Néha a Meta.fields megadása nem elég, nem garantalja, hogy a form input alkalmazva lesz
    # Ehelyett fent explicit módon is definiálhatjuk a mezőket
    # Ha explicit mező definíció van , akkor a meta widget felesleges
    class Meta:
        model = BlogPost
        fields = {
            "title": ["exact"],
            # "content": ["icontains"],
        }
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cím keresése'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tartalom keresése'}),
        # }

