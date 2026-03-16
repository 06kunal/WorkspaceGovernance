from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework import serializers

# for generating token for email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    
    role = serializers.ChoiceField(choices=["EMP", "OWN"])
    
    class Meta:
        model = User
        fields = ["username", "email", "role"]
    
    
    def create(self, validated_data):


        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            role = validated_data["role"],
            is_active=False
        )
        
        
        # generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        invite_link = f"http://localhost:8000/set-password/{uid}/{token}/"

        send_mail(
            subject="Workspace Invitation",
            message=f"You have been invited. Set your password here:\n{invite_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        

        return user





class SetPasswordSerializer(serializers.Serializer):

    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def save(self, user):

        password = self.validated_data["password1"]

        user.set_password(password)
        user.is_active = True
        user.save()

        return user




# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     active = serializers.BooleanField(default=False)
    
    
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2', 'active']
#         extra_kwargs = {
#             'password':{'write_only': True}
#         }
        
    
#     #validate is called autmatically when we call serializer.is_valid()
#     def validate(self, attrs):
        
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {
#                     'error': 'p1 and p1 shoudl be same!'
#                 }
#             )
            
#         #checking if email already exists
#         if User.objects.filter(email=attrs['email']).exists():
#             raise serializers.ValidationError({'error':'user already exists!'})
                
#         return attrs
    
    
#     def create(self, validated_data):
#         password = validated_data.pop('password2')
        
        
#         user = User(email=self.validated_data['email'], username=self.validated_data['username'])
#         user.set_password(password)
#         user.save()
        
#         return user
        
        
        
        
        
        

            
        