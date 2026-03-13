from django.contrib.auth.models import User
from rest_framework import serializers

from company_app.models import WorkSpaceUser


class UserCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=["EMP", "MNG", "HOD"])
    
    class Meta:
        model = User
        fields = ["username", "email", "role"]
    
    
    def create(self, validated_data):

        role = validated_data.pop("role")

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            is_active=False
        )

        WorkSpaceUser.objects.create(
            user=user,
            role=role,
            workspace=self.context["workspace"]
        )

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
        
        
        
        
        
        

            
        