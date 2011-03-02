from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model

try:
    from configstore.configs import get_config
    use_configstore = True
except ImprotError:
    use_configstore = False

def get_user_profile(user):
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        ProfileClass = get_model(app_label, model_name)
        return Profile.objects.create(user=user)

def get_facebook_settings():
    ''' Get the Facebook app credentials. First try django-configstore, fallback to settings.
        Returns a tuple (APP_ID, APP_SECRET)
    '''
    if use_configstore:
        config = get_config('fbi-credentials')
        return (config.get('app_id'), config.get('app_secret'))
    return (getattr(settings, 'FACEBOOK_APP_ID', None), getattr(settings, 'FACEBOOK_APP_SECRET', None))
