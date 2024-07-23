from django.contrib.auth import authenticate
from rest_framework.fields import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from django.http import HttpResponse, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import os
from .serializers import UserRegistrationSerializer,UserLoginSerializer,UserDownloadLinkSerializer,UserFileSerializer,UploadFileSerialzer
from .models import User, File, DownloadLink
from .utils import decrypt_url


from rest_framework_simplejwt.tokens import RefreshToken

# genertae token manually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Registration view
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token =get_tokens_for_user(user)
            return Response({"token":token, "Msg": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                # Generate and return JWT tokens
                token =get_tokens_for_user(user)
                return Response({"token": token, "Msg":'Login Successfuly'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# File upload view
@permission_classes([IsAuthenticated])
class UserFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        file_serializer = UserFileSerializer(data=request.data)
        if file_serializer.is_valid(raise_exception=True):
            user_type = request.data.get('user_type')
            if user_type != 'Ops':
                raise PermissionDenied({"error": "Only Ops users can upload files"})
            else:
                uploaded_by_id = request.data.get('uploaded_by')
                try:
                    uploaded_by = User.objects.get(id=uploaded_by_id)
                except User.DoesNotExist:
                    return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

                file_instance = file_serializer.save(uploaded_by=uploaded_by)
                return Response({"Msg": "File Uploaded Successfully!"}, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Generate download link view
@permission_classes([IsAuthenticated])
class GenertaorDownLoadLink(APIView):
    def post(self, request, format=None):
        serializer = UserDownloadLinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            client_user_id = request.data.get('client_user')
            try:
                client_user = User.objects.get(id=client_user_id)
            except User.DoesNotExist:
                return Response({"error": "Client user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if client_user.user_type != 'Client':
                raise PermissionDenied({"error": "Only client users can access the link of download files"})

            download_link = serializer.save()
            return Response({"data": serializer.data, "Msg": "URL generated successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# view to list all upload files

class UploadFilesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        # Ensure only 'Client' users can access this view
        if user.user_type != 'Client':
            raise PermissionDenied({"error": "Only client users can access the list of files"})

        files = File.objects.all()  # Retrieve all files
        serializer = UploadFileSerialzer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Download file view

@permission_classes([IsAuthenticated])
class DownloadFileView(APIView):
    def get(self, request, encrypted_string):
        try:
            file_id = decrypt_url(encrypted_string)
            download_link = DownloadLink.objects.get(id=file_id)

            # Check if the file exists
            file_path = os.path.join(settings.MEDIA_ROOT, download_link.file.name)
            if not os.path.exists(file_path):
                raise Http404("File does not exist")

            # Serve the file
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response

        except DownloadLink.DoesNotExist:
            return Response({"error": "Invalid download link."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



