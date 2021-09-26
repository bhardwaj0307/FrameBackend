from django.apps import AppConfig


class User2FaConfig(AppConfig):
    name = 'user_2FA'

    def ready(self):
        import user_2FA.post_signals

