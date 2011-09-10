
__author__ = 'Derek Payton <derek@cukerinteractive.com>'
__copyright__ = 'Copyright (c) Derek Payton and Cuker Interactive'
__description__ = 'Django+Facebook authentication with pluggable backends so you can integrate with facebook on your own terms'
__version__ = '0.1a'

try:
    from django_fbi import configforms
    USE_CONFIGSTORE = True
except ImportError:
    USE_CONFIGSTORE = False
