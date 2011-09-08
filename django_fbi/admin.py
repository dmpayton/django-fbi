from django import forms
from django.contrib import admin
from django.template import loader
from django.template.base import TemplateDoesNotExist
from django_fbi.models import FacebookApp, FacebookAccount

class FacebookAppForm(forms.ModelForm):

    def _validate_template(self, template):
        if template:
            try:
                loader.find_template(template)
            except TemplateDoesNotExist:
                raise forms.ValidationError('Template does not exist.')
            return True

    def clean_canvas_template(self):
        template = self.cleaned_data.get('canvas_template')
        self._validate_template(template)
        return template

    def clean_tab_template(self):
        template = self.cleaned_data.get('tab_template')
        self._validate_template(template)
        return template

    class Meta:
        model = FacebookApp

class FacebookAppAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('namespace', 'connect')
        }),
        ('App Credentials', {
            'fields': ('app_id', 'app_secret', 'scope')
        }),
        ('Canvas Page', {
            'fields': ('canvas_template', 'canvas_content')
        }),
        ('Tab Page', {
            'fields': ('tab_template', 'tab_content')
        }),
    )
    form = FacebookAppForm
    list_display = ('namespace', 'app_id', 'connect')
    list_editable = ('connect',)

admin.site.register(FacebookApp, FacebookAppAdmin)
admin.site.register(FacebookAccount)
