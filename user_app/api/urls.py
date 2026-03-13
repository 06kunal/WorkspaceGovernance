from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from user_app.api.views import InviteUserView


urlpatterns = [ 
    path('invite/', InviteUserView.as_view(), name='register'),
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # refresh token
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]