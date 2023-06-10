import hashlib
from django.utils.translation import ugettext_noop as _
from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
from django.utils.datastructures import OrderedDict

class SHA256PasswordHasher(BasePasswordHasher):
    algorithm = "sha256"