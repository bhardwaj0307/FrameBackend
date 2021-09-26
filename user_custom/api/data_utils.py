import datetime
import locale

from django.utils.timezone import now

# from crm_mortgage.models import Mortgage
# from crm_user_profiles.models import CrmUserProfiles, Occasion
from user_custom.models import User


def current_date():
    return now().date()


locale.setlocale(locale.LC_ALL, '')


class UserDataUtils(object):

    def get_all_data_utils(self, super_user):
        if super_user.is_superuser:
            return list(User.objects.values('id', 'name', 'email'))
        else:
            return User.objects.filter(id=super_user.id).values("id", "name", "email")

    def get_single_one_data_utils(self, pk, user_data):
        obj = None
        try:
            if user_data.is_superuser:
                obj = User.objects.filter(id=pk).values('id', 'name', 'email', 'is_active', 'is_superuser')
            else:
                obj = User.objects.filter(id=user_data.id).values('id', 'name', 'email', 'is_active', 'is_superuser')
        except:
            pass
        return obj

    def get_single_new_data_utils(self, pk):
        obj = None
        try:
            obj = User.objects.filter(id=pk).values('id', 'name', 'email', "is_active", "is_superuser")
            print(obj)
        except:
            pass
        return obj

    def create_one_data_utils(self, **data):
        obj_status = False
        try:
            a = User.objects.create(**data)
        except:
            pass
        return a.id

    def update_user_data_utils(self, logged_person_id, **data):
        obj = User.objects.filter(id=logged_person_id).update(**data)
        status = True if obj == 1 else False
        return status

    def delete_user_data_utils(self, pk, user_data):
        obj_status = False
        try:
            if user_data.is_superuser or int(pk) == user_data.id:
                obj = User.objects.get(id=pk)
                obj.delete()
                obj_status = True
        except:
            pass
        return obj_status

    def get_current_user_data_utils(self, logged_person_id):
        obj = None
        try:

            obj = list(
                User.objects.filter(id=logged_person_id).values('id', 'name', 'email', 'is_superuser', "is_active"))
        except:
            pass
        return obj

    def get_users_exclude_logged_user(self, logged_person_id):
        user_obj = User.objects.filter(id=logged_person_id, is_superuser=True)
        obj = None
        if user_obj:
            try:
                obj = User.objects.exclude(id=logged_person_id).exclude(name="").values('id', 'name', 'email',
                                                                                        "is_superuser", "is_active")
            except:
                obj = 1
        return obj
