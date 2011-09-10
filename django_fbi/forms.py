from django import forms
from django.template import loader
from django.template.base import TemplateDoesNotExist
from django_fbi.models import FacebookApp

class FacebookAppAdminForm(forms.ModelForm):
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
