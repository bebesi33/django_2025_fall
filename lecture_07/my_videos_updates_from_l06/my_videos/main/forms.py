from django import forms
from .models import Video
from django.forms import ModelForm
import logging

logger = logging.getLogger(__file__)


def check_video_existence(title, url):
    if Video.objects.filter(title__iexact=title, url__iexact=url).exists():
        raise forms.ValidationError("Már van ilyen videó!")


class VideoForm(ModelForm):
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
        print(cleaned_data)
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
            check_video_existence(title, url)

        return cleaned_data


class ModifyVideoForm(VideoForm):

    def __init__(self, data, instance, orig_title, orig_url):
        super().__init__(data=data, instance=instance)
        self.orig_url = orig_url
        self.orig_title = orig_title

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        if self.orig_title != self.cleaned_data.get(
            "title"
        ) or self.orig_url != self.cleaned_data.get("url"):
            check_video_existence(
                self.cleaned_data.get("title"), self.cleaned_data.get("url")
            )
        return cleaned_data
