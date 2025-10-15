try:
    from django.contrib import admin
except Exception:
    # Fallback minimal admin shim for editors or environments without Django installed
    class _DummySite:
        def register(self, model):
            # no-op in non-Django environment
            return None
    class _DummyAdmin:
        site = _DummySite()
    admin = _DummyAdmin()

from .models import History

# Register your models here.
try:
    admin.site.register(History)
except Exception:
    # Ignore registration errors when running outside a Django runtime
    pass
# python manage.py makemigrations
# python manage.py migrate

