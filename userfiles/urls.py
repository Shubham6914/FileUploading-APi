from django.urls import path
from .views import UserRegistrationView, UserLoginView,UserFileUploadView,GenertaorDownLoadLink,DownloadFileView,UploadFilesView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('upload/', UserFileUploadView.as_view(), name='file_upload'),
    path('generate_url/', GenertaorDownLoadLink.as_view(), name='generate_encrypted_url'),
    path('download/<str:encrypted_string>/', DownloadFileView.as_view(), name='download_file'),
    path('list_files/',UploadFilesView.as_view(),name='file_lists'),
    
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
