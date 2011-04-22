from django.conf import settings

ADMIN_EMAIL_MASK_PATTERNS = getattr(settings, 
    'ADMIN_EMAIL_MASK_PATTERNS', 
    (('ccregex', '****************'), ))
