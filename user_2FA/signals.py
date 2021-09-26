import django.dispatch

__all__ = [
    'reset_password_token_created',

]

reset_password_token_created = django.dispatch.Signal(
    providing_args=["instance", "reset_password_token"],
)

