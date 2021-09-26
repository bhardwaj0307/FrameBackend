from django.contrib.auth.hashers import make_password

from user_custom.api.data_utils import UserDataUtils


class UserUtils(object):
    data_class = UserDataUtils()

    def get_utils(self, super_user):
        return self.data_class.get_all_data_utils(super_user)

    def get_single_one_utils(self, pk, user_data):
        return self.data_class.get_single_one_data_utils(pk, user_data)

    def get_single_new_utils(self, pk):
        return self.data_class.get_single_new_data_utils(pk)

    def create_user_utils(self, **data):
        cap = data["name"]
        a = cap.title()
        del data["name"]
        data["name"] = a
        fetch_password = data["password"]
        del data["password"]
        password = make_password(fetch_password)
        data["password"] = password

        return self.data_class.create_one_data_utils(**data)

    def update_user_utils(self, logged_person_id, **data):
        cap = data["name"]
        a = cap.title()
        del data["name"]
        data["name"] = a
        fetch_password = data["password"]
        del data["password"]
        password = make_password(fetch_password)
        data["password"] = password
        return self.data_class.update_user_data_utils(logged_person_id, **data)

    def delete_user_utils(self, pk, user_data):
        return self.data_class.delete_user_data_utils(pk, user_data)

    def get_current_user_utils(self, logged_person_id):
        return self.data_class.get_current_user_data_utils(logged_person_id)

    def get_users_exclude_logged_user_utils(self, logged_person_id):
        return self.data_class.get_users_exclude_logged_user(logged_person_id)

    def get_notes_data(self, logged_person_id, **args):
        return self.data_class.get_notes_data(logged_person_id, **args)

    def get_rate_review_data(self, logged_person_id, **args):
        return self.data_class.get_rate_review_data(logged_person_id, **args)


