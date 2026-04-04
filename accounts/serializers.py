from rest_framework  import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True,required=True,min_length=8)
    password2 = serializers.CharField(write_only=True,required=True,min_length=8)  

    class Meta:
        model = User
        fields = ['email','username','password','password2']
    
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return data

    def create(self,validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password']
        )
        return user
