from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'


    #file is initialized when the django applicatio is launched by the internal django application
    #registry
    #handlers will now be called for every new product imag uploaded to the site
    def ready(self):
        from . import signals
