from django.conf import settings
from rest_framework import status, serializers, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import *

__all__ = [
    "create_address",
    "update_address",
    "get_all_address",
    "address_by_id",
    "delete_address_by_id"
]


class CreateAddress(GenericAPIView):
    """
    An Api Which Create Address Of logged User
    """
    throttle_classes = ()
    # permission_classes = ()
    serializer_class = CreateAddressSerializer
    queryset = ""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, primary=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateAddress(GenericAPIView):
    """
    An Api View which Update Address with Address_id of logged User
    """
    throttle_classes = ()
    # permission_classes = ()
    serializer_class = UpdateAddressSerializer

    def put(self, request, address_id):
        logged_person_id = request.user.id
        address_obj = Address.objects.filter(id=address_id).filter(user_id=logged_person_id)
        if not address_obj:
            response = {"success": False,
                        "message": ' Sorry no address has id :{}'.format(address_obj)}
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer = UpdateAddressSerializer(address_obj, data=request.data, partial=True)
            if serializer.is_valid():
                address_update = Address.objects.filter(id=address_id).update(**request.data)
                response = {"success": True,
                            "message": "The Address has been Updated.",
                            }
                status_code = status.HTTP_201_CREATED
            else:
                response = {"success": False,
                            "errors": serializer.errors}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response, status=status_code)


class GetAllAddress(GenericAPIView):
    """
    Get all Address of logged User
    """

    def get(self, request, *args, **kwargs):
        response = {"success": False, 'data': [],
                    "message": '!!! Ops no data found. '}
        status_code = status.HTTP_400_BAD_REQUEST
        logged_user_id = request.user.id
        data = Address.objects.filter(user_id=logged_user_id).values()
        if len(data) > 0:
            response.update({'data': data, 'success': True})
            response.update({'message': 'data received from db '})
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class GetAddressById(GenericAPIView):
    """
    Get Address by Id of logged User
    """

    def get(self, request, address_id):
        response = {"success": False, 'data': [],
                    "message": '!!! Ops no data found. '}
        status_code = status.HTTP_400_BAD_REQUEST
        logged_user_id = request.user.id
        data = Address.objects.filter(id=address_id).filter(user_id=logged_user_id).values()
        if len(data) > 0:
            response.update({'data': data, 'success': True})
            response.update({'message': 'data received from db '})
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class DeleteAddress(GenericAPIView):
    """
    Delete Address
    """

    def delete(self, request, address_id):
        response = {"success": False, 'data': [],
                    "message": '!!! Ops no data found. '}
        status_code = status.HTTP_400_BAD_REQUEST
        logged_user_id = request.user.id
        data = Address.objects.filter(id=address_id).filter(user_id=logged_user_id)
        if len(data) > 0:
            delete_obj = data.delete()
            response.update({'data': [], 'success': True})
            response.update({'message': 'Address Deleted Successfully'})
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


create_address = CreateAddress.as_view()
update_address = UpdateAddress.as_view()
get_all_address = GetAllAddress.as_view()
address_by_id = GetAddressById.as_view()
delete_address_by_id = DeleteAddress.as_view()
