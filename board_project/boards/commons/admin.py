from django import forms
from django.contrib import admin
from django.db import models


class SiteBaseModelAdmin(admin.ModelAdmin):
    formfield_overrides = (
        {
            models.TextField: {"widget": forms.Textarea(attrs={"rows": 4, "cols": 80})},
            models.CharField: {"widget": forms.TextInput(attrs={"class": "form-control"})},
        }
    )

    list_per_page = 50
    list_max_show_all = 500

    save_as = True
    save_as_continue = False
    save_on_top = True
    save_on_bottom = False

    preserve_filters = True

    actions_on_top = False
    actions_on_bottom = True
