from datetime import date
from .models import User


class MyMixin:

    def get_user_birth_info(self):
        users = User.objects.filter(birth_day=date.today())
        if users.exists():
            for u in users:
                info = (
                    u.pk,
                    u.get_full_name(),
                    u.birth_day,
                    u.email,
                )
                yield info

    def get_emails(self):
        for u in User.objects.all().exclude(email=''):
            info = (
                u.pk,
                u.get_full_name(),
                u.email,
            )
            yield info
