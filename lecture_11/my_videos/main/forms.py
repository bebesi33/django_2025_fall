from django import forms
from .models import Video
from urllib.parse import urlparse


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "url", "description", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    # clean_<mezőnév> metódusok egyedi mezőszintű validáláshoz
    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError(
                "A címnek legalább 5 karakter hosszúnak kell lennie."
            )
        return title

    def clean_url(self):
        url = self.cleaned_data.get("url")
        if url:
            parsed = urlparse(url)
            if not parsed.scheme.startswith("http"):
                raise forms.ValidationError(
                    "Az URL-nek http vagy https sémát kell használnia."
                )
        return url

    # -> Formszintű validálás
    # A clean() metódus az egész formra vonatkozó validálást végzi
    # Először a mezőszintű validálás fut le, majd ha az sikeres, akkor a formszintű
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        url = cleaned_data.get("url")

        # Ne lehessen duplikált (title, url) páros
        if title and url:
            if Video.objects.filter(title__iexact=title, url__iexact=url).exists():
                # ValidationError kell ha sikertelen
                raise forms.ValidationError("Ez a videó már létezik az adatbázisban.")

        return cleaned_data
