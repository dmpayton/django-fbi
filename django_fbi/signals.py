from django.dispatch import Signal

facebook_login = Signal(providing_args=('account',))
facebook_connect = Signal(providing_args=('account',))
facebook_deauthorize = Signal(providing_args=('account',))
