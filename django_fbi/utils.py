from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model

def get_user_profile(user):
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
        ProfileClass = get_model(app_label, model_name)
        return Profile.objects.create(user=user)
