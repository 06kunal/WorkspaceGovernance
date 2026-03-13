from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user_app import models
from user_app.api.permissions import CanCreateUser
from company_app.models import WorkSpace
from user_app.api.serializers import UserCreateSerializer




class InviteUserView(APIView):

    permission_classes = [IsAuthenticated, CanCreateUser]

    def post(self, request, workspace_id):

        workspace = WorkSpace.objects.get(id=workspace_id)

        serializer = UserCreateSerializer(
            data=request.data,
            context={"workspace": workspace}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User invited successfully"},
            status=status.HTTP_201_CREATED
        )





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
        
        