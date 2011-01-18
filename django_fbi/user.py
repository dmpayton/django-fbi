import datetime
import re
from django.conf import settings
from django.core.mail import send_mail, mail_admins
from django.forms.util import ValidationError
from facebook import GraphAPI, GraphAPIError

class FacebookUser(GraphAPI):
    def __init__(self, user):
        super(FacebookUser, self).__init__(user['access_token'])
        self._is_authenticated = None
        self._profile = None

    def is_authenticated(self):
        if self._is_authenticated is None:
            try:
                self.profile
                self._is_authenticated = True
            except GraphAPIError, err:
                self._is_authenticated = False
        return self._is_authenticated

    @property
    def profile(self):
        if self._profile is None:
            self._profile = self.get_object('me')
            self._profile['facebook_id'] = self._profile['id']
            self._profile['website'] = self._extract_url(self._profile.get('website'))
            self._profile['image'] = 'https://graph.facebook.com/me/picture?type=large&access_token=%s' % self.access_token
            self._profile['image_thumb'] = 'https://graph.facebook.com/me/picture?access_token=%s' % self.access_token
        return self._profile


    def _extract_url(cself, text_url_field):
        '''
        >>> url_text = 'http://www.google.com blabla'
        >>> FacebookUser._extract_url(url_text)
        u'http://www.google.com/'

        >>> url_text = 'http://www.google.com/'
        >>> FacebookUser._extract_url(url_text)
        u'http://www.google.com/'

        >>> url_text = 'google.com/'
        >>> FacebookUser._extract_url(url_text)
        u'http://google.com/'

        >>> url_text = 'http://www.fahiolista.com/www.myspace.com/www.google.com'
        >>> FacebookUser._extract_url(url_text)
        u'http://www.fahiolista.com/www.myspace.com/www.google.com'
        '''
        text_url_field = str(text_url_field)
        seperation = re.compile('[ |,|;]+')
        parts = seperation.split(text_url_field)
        for part in parts:
            from django.forms import URLField
            url_check = URLField(verify_exists=False)
            try:
                clean_url = url_check.clean(part)
                return clean_url
            except ValidationError, e:
                continue
