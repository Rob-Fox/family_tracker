import hashlib
from django.utils.translation import ugettext_noop as _
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash, make_password, check_password
from django.utils.datastructures import OrderedDict

class PasswordHasher():
    def encode(self, password, salt, iterations=None):
        assert password is not None
        return make_password(password, salt,  hasher='default')

    def verify(self, password, encoded_password):
        assert password is not None and encoded_password is not None
        return check_password(password, encoded_password, setter=None, preferred='default')
        