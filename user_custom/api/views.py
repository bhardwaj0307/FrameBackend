from datetime import timedelta

from django.conf import settings
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_rest_passwordreset.models import ResetPasswordToken, get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import pre_password_reset, post_password_reset
from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from user_profile.models import *
from user_custom.api.serializers import PasswordTokenSerializer
from user_custom.api.serializers import UserSerializer
from user_custom.api.utils import UserUtils
from user_custom.models import User
# from crm_user_profiles.models import CrmUserProfiles
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group


# from crm_management.models import Package

class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UsersApiCreateRead(ViewSet):
    # authentication_classes = ()
    data_class = UserUtils()
    permission_classes_by_action = {'create_user': [AllowAny], 'check_email_admin': [AllowAny]}

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_all_user(self, request):
        response = {"success": False, 'data': [],
                    "message": '!!! Ops no data found. '}
        status_code = status.HTTP_400_BAD_REQUEST
        super_user = request.user
        data = self.data_class.get_utils(super_user)
        if len(data) > 0:
            if super_user.is_superuser:
                response.update({'data': data, 'success': True})
                response.update({'message': 'data received from db '})
                status_code = status.HTTP_200_OK
            elif not super_user.is_superuser:
                response.update({'data': data, 'success': True})
                response.update({'message': 'User is not Superuser'})
                status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def create_user(self, request):
        password = request.data["password"]
        password1 = request.data["password1"]
        email = request.data["email"]
        qs = User.objects.filter(email=email)
        if qs.exists():
            response = {"success": False,
                        "errors": "Email Already Exists"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE

        elif password == password1:
            del request.data["password1"]

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                pk = self.data_class.create_user_utils(**request.data)
                user_obj = self.data_class.get_single_new_utils(pk)
                if user_obj:
                    response = {"success": True,
                                "message": "The User has been created.",
                                'data': user_obj}
                    status_code = status.HTTP_201_CREATED
            else:
                response = {"success": False,
                            "errors": serializer.errors}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif password != password1:
            response = {"success": False,
                        "errors": "Password Must be same"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response, status=status_code)

    def edit_user(self, request, *args, **kwargs):
        logged_person_id = request.user.id
        self.object = self.get_object()
        # user = User.objects.filter(id=logged_person_id)
        old_password = request.data["old_password"]
        if not self.object.check_password(old_password):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        del request.data["old_password"]
        password = request.data["password"]
        password1 = request.data["password1"]
        email = request.data["email"]
        qs = User.objects.filter(email=email).exclude(id=logged_person_id)
        if qs.exists():
            response = {"success": False,
                        "errors": "Email Already Exists"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE

        elif password == password1:
            del request.data["password1"]
            User.objects.filter(id=logged_person_id).update(email=None)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                pk = self.data_class.update_user_utils(logged_person_id, **request.data)
                response = {"success": True,
                            "message": "The User has been Updated.",
                            }
                status_code = status.HTTP_201_CREATED
            else:
                response = {"success": False,
                            "errors": serializer.errors}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif password != password1:
            response = {"success": False,
                        "errors": "Password Must be same"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response, status=status_code)

    def specific_user(self, request, pk):
        response = {"success": False,
                    "message": ' Sorry no user has id :{}'.format(pk)}
        status_code = status.HTTP_400_BAD_REQUEST
        user_data = request.user
        mortgage_obj = self.data_class.get_single_one_utils(pk, user_data)
        if mortgage_obj:
            if user_data.is_superuser:
                response.update({'success': True})
                response.update({'message': 'User retrieved successfully'})
                response.update({'data': mortgage_obj})
                status_code = status.HTTP_200_OK
            elif not user_data.is_superuser:
                response.update({'success': True})
                response.update({'message': 'User is not SuperUser, Permission Issue'})
                response.update({'data': mortgage_obj})
                status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def delete_user(self, request, pk):
        response = {"success": False,
                    "message": '!!! Ops something went wrong '}
        status_code = status.HTTP_400_BAD_REQUEST
        user_data = request.user
        if not user_data.is_superuser and int(pk) != user_data.id:
            response.update({'success': False})
            response.update({'message': 'User is not Superuser , Permission Denied'})
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        mortgage_status = self.data_class.delete_user_utils(pk, user_data)
        if mortgage_status:
            response.update({'success': True})
            response.update({'message': 'User deleted successfully'})
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_current_user(self, request):
        response = {"success": False,
                    "message": '!!! Ops something went wrong '}
        status_code = status.HTTP_400_BAD_REQUEST
        logged_person_id = request.user.id
        mortgage_obj = self.data_class.get_current_user_utils(logged_person_id)
        if mortgage_obj:
            obj = list(Profile.objects.filter(user_id=logged_person_id).values())
            for profile_obj in obj:
                mortgage_obj[0]["birth_date"] = profile_obj["birth_date"]
                mortgage_obj[0]["gender"] = profile_obj["gender"]
                mortgage_obj[0]["about"] = profile_obj["about"]
                mortgage_obj[0]["profile_picture"] = profile_obj["profile_picture"]
            response = {"success": True, 'data': mortgage_obj,
                        "message": 'Login User Detail '}
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_users_exclude_logged_user(self, request):
        logged_person_id = request.user.id
        users_obj = self.data_class.get_users_exclude_logged_user_utils(logged_person_id)
        if users_obj is None:
            response = {"success": False,
                        "message": '!!! User is not SuperUser'}
            status_code = status.HTTP_400_BAD_REQUEST
        if users_obj == 1:
            response = {"success": False,
                        "message": '!!! No Users Found'}
            status_code = status.HTTP_404_NOT_FOUND
        if users_obj:
            response = {"success": True, 'data': users_obj,
                        "message": 'Users Details Exclude Logged User '}
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def change_status_of_user(self, request, user_id, user_status):
        user_obj = None
        logged_person_id = request.user
        logged_user_obj = logged_person_id.is_superuser
        if int(user_status) == 0:
            user_status = True
        elif int(user_status) == 1:
            user_status = False
        if logged_user_obj:
            user_obj = User.objects.filter(id=user_id)
        elif not logged_user_obj:
            response = {"success": False,
                        "message": '!!! Current User is not SuperUser'}
            status_code = status.HTTP_400_BAD_REQUEST
        if user_obj:
            update_user_obj = user_obj.update(is_active=user_status)
            response = {"success": True,
                        "message": 'User Status Update'}
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def check_email_admin(self, request):
        response = {"success": False,
                    "message": '!!! Ops something went wrong '}
        status_code = status.HTTP_400_BAD_REQUEST
        email = request.GET.get("email")
        if email:
            email = email.lower()
            crm_obj = User.objects.all().values_list("email", flat=True)
            crm_obj = list(filter(None, crm_obj))
            crm_obj = list(filter(str.strip, crm_obj))
            crm_obj = [x.lower() for x in crm_obj]
            if crm_obj:
                response = {"success": True,
                            "message": 'Email Exists Data '}
                status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class ResetPasswordConfirm(ViewSet):
    """
    An Api View which provides a method to reset a password based on a unique token
    """
    # throttle_classes = ()
    # permission_classes = ()
    serializer_class = PasswordTokenSerializer
    permission_classes_by_action = {'forget_password': [AllowAny]}

    def forget_password(self, request, token_auth):
        token = token_auth

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'Incorrect Token'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': ' Token expired'}, status=status.HTTP_404_NOT_FOUND)

        # change users password (if we got to this code it means that the user is_active)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        password2 = serializer.validated_data['password2']

        if password != password2:
            return Response({'status': 'Password must be same '}, status=status.HTTP_404_NOT_FOUND)
        else:
            if reset_password_token.user.eligible_for_reset():
                pre_password_reset.send(sender=self.__class__, user=reset_password_token.user)
                try:
                    # validate the password against existing validators
                    validate_password(
                        password,
                        user=reset_password_token.user,
                        password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
                    )
                except ValidationError as e:
                    # raise a validation error for the serializer
                    raise exceptions.ValidationError({
                        'password': e.messages
                    })

                reset_password_token.user.set_password(password)
                reset_password_token.user.save()
                post_password_reset.send(sender=self.__class__, user=reset_password_token.user)

            # Delete all password reset tokens for this user
            ResetPasswordToken.objects.filter(user=reset_password_token.user).delete()

            return Response({'status': 'Successfully Change'})

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
