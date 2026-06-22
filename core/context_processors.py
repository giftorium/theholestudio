from .models import HomePage


def site_settings(request):
    return {'site_settings': HomePage.get()}
