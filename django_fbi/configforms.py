from configstore.configs import ConfigurationInstance, register
from configstore.forms import ConfigurationForm
from django import forms

class FacebookAuthInfoForm(ConfigurationForm):
    app_id = forms.CharField(max_length=50)
    app_secret = forms.CharField(max_length=255)
    scope = forms.CharField(max_length=255, help_text='')

instance = ConfigurationInstance('fb-auth', 'Facebook Auth Credentials', FacebookAuthInfoForm)
register(instance)
