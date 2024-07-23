from django.db import IntegrityError
from rest_framework import serializers
from .models import User, File, DownloadLink
from .utils import generate_encrypted_url


# Serializer class for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "user_type", "password", "password2", "is_verified"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True}  # Assuming `is_verified` is set to `False` by default
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove password2 from validated_data
        user = User.objects.create_user(**validated_data)
        return user


# Login serializer for user
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email", "password"]


# File serializer
class UserFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file', 'file_type', 'uploaded_by']
        read_only_fields = ['uploaded_by']

    def validate_file_type(self, value):
        allowed_types = ['pptx', 'docx', 'xlsx']
        if not any(value.endswith(ext) for ext in allowed_types):
            raise serializers.ValidationError("File type is not allowed.")
        return value


#  this serialzer for showing all upload files

class UploadFileSerialzer(serializers.ModelSerializer):
    uploaded_by_name = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = fields = ['file_name', 'file', 'file_type', 'uploaded_by','uploaded_by_name']
        
    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.name if obj.uploaded_by else None

# Download serializer
class UserDownloadLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadLink
        fields = ["file", "client_user", "encrypted_url", "created_at", "expires_at"]
        read_only_fields = ['encrypted_url']

    def create(self, validated_data):
        # Ensure valid `encrypted_url` is generated
        download_link = DownloadLink(**validated_data)
        encrypted_url = generate_encrypted_url(download_link)

        if not encrypted_url:
            raise serializers.ValidationError({"encrypted_url": "Generated URL is empty or invalid."})
        
        download_link.encrypted_url = encrypted_url
        try:
            download_link.save()
        except IntegrityError:
            raise serializers.ValidationError({"encrypted_url": "Duplicate entry for the encrypted URL."})

        return download_link
