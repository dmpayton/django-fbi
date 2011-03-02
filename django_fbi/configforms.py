from configstore.configs import ConfigurationInstance, register
from configstore.forms import ConfigurationForm
from django import forms
from django.contrib.auth.models import User

class FacebookAppCredentialsForm(ConfigurationForm):
    app_id = forms.CharField(max_length=50)
    app_secret = forms.CharField(max_length=250)

instance = ConfigurationInstance('fbi-credentials', 'Facebook App Credentials', FacebookAppCredentialsForm)
register(instance)
