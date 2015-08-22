from django.conf import settings
from django.utils.importlib import import_module

for app in settings.INSTALLED_APPS:
    print app
    try:
        import_module('%s.analytics' % app)
    except:
        pass
