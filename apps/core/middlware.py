from django.utils import translation
from django.conf import settings

class LanguageMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = None
        if request.user.is_authenticated and hasattr(request.user, "language"):
            lang = request.user.language

        elif "lang" in request.GET:
            lang = request.GET.get("lang")

        elif request.META.get("HTTP_ACCEPT_LANGUAGE"):
            lang = request.META.get("HTTP_ACCEPT_LANGUAGE").split(",")[0]

        if not lang:
            lang = settings.LANGUAGE_CODE

        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        return response