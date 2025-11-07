from .models import Video
from django import forms
import logging

logger = logging.getLogger(__file__)


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

    # self.is_bound? Ture ha töltve van és false ha NotImplemented
    # self.errors v. _errors? lsita, ha van elem akkor PythonFinalizationError
    # self.is_bound és len(errors) > 0 -> akkor nem valid

    def clean_title(self):
        # clean_<mezőnév> -> adott mező vizsgálata...
        title = self.cleaned_data.get("title", "")
        logger.warning("clean_title started")
        if len(title) < 5:
            raise forms.ValidationError(
                "A címnek legalább 5 karakter hosszúnak kell lennie."
            )
        return title

    def clean_description(self):
        # clean_<mezőnév> -> adott mező vizsgálata...
        description = self.cleaned_data.get("description", "")
        logger.warning("clean_description started")
        if len(description) < 15:
            raise forms.ValidationError(
                "A leírásnak legalább 15 karakter hosszúnak kell lennie."
            )
        return description

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        url = cleaned_data.get("url")
        logger.warning("form level clean method started")

        if title and url:
            logger.warning(f"Title: {title}")
            logger.warning(f"URL: {url}")
            vals = Video.objects.filter(url__exact=url).values()
            logger.warning(vals)
            vals = Video.objects.filter(title__exact=title).values()
            logger.warning(vals)
            if Video.objects.filter(title__iexact=title, url__iexact=url).exists():
                raise forms.ValidationError("Már van ilyen videó!")

        return cleaned_data
