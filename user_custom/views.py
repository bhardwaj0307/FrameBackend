# import pyotp
#
#
# def generateOTP():
#     global totp
#     secret = pyotp.random_base32()
#     # set interval(time of the otp expiration) according to your need in seconds.
#     totp = pyotp.TOTP(secret, interval=300)
#     one_time = totp.now()
#     return one_time
#
# def verifyOTP(one_time):
#     answer = totp.verify(one_time)
#     return answer
#
# message = f'Welcome {first_name} Your OTP is : ' + \
#                     generateOTP()
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [email]
#                 message = message
#                 subject = "OTP"
#                 send_mail(
#                     subject,
#                     message,
#                     email_from,
#                     recipient_list,
#                     fail_silently=False,
#                 )
#
#
# class VerifyOTPView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = VerifyOTPSerializer
#
#     def post(self, request):
#         serializer = VerifyOTPSerializer(data=request.data)
#         email = request.data['email']
#         one_time = request.data['otp']
#         print('one_time_password', one_time)
#         one = verifyOTP(one_time)
#         print('one', one)
#         if one:
#             MyUser.objects.filter(email=email).update(
#                 is_confirmed=True, is_used=True, otp=one_time)
#             return Response({'msg': 'OTP verfication successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'msg': 'OTP verfication Failed'}, status=status.HTTP_400_BAD_REQUEST)