from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user_app import models
# from user_app.api.permissions import CanCreateUser
from company_app.models import WorkSpace
from user_app.api.serializers import UserCreateSerializer, SetPasswordSerializer


# for token for email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


User = get_user_model()




class InviteUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role != "OWN":
            return Response({"error": "Only owners can create users"}, status=403)

        serializer = UserCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User invited successfully"},
            status=status.HTTP_201_CREATED
        )


class SetPasswordView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token invalid or expired"}, status=400)

        serializer = SetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user)
            return Response({"message": "Password set successfully"})

        return Response(serializer.errors, status=400)




# @api_view(['POST', ])
# def registration_view(request):
    
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data) # Passing the data from the request to our serializer.
        
#         data = {} #created an empty dictionary and then we will append everything in this dict.
        
#         if serializer.is_valid():
#             account = serializer.save()
            
#             data['Response'] = "Regsitration Successful! Waiting for Admin approval"
#             # Creating token for the user. will create a token after the user gets admin approval.
#             # data['Response'] = "Regsitration Successful!"
#             # data['username'] = account.username
#             # data['email'] = account.email

#             # refresh = RefreshToken.for_user(account)

#             # data['token'] = {
#             #     'refresh': str(refresh),
#             #     'access': str(refresh.access_token),
#             # }
                        
#         else:
#             data = serializer.errors
            
#         return Response(data, status=status.HTTP_201_CREATED) 
        
        