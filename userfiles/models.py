from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, user_type, password=None,Password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, user_type, password=None):
        user = self.create_user(
           
           email,
           password = password,
           name = name,
           user_type = user_type,
   
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('Ops', 'Ops User'),
        ('Client', 'Client User'),
    )
    name = models.CharField(max_length=85)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES) 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type']

    def __str__(self):
      return self.email

    def has_perm(self, perm, obj=None):
      return True

    def has_module_perms(self, app_label):
      return True

    @property
    def is_staff(self):
      #  all admins are staff
      return self.is_admin


class File(models.Model):
    FILE_TYPE_CHOICES = (
        ('pptx', 'PPTX'),
        ('docx', 'DOCX'),
        ('xlsx', 'XLSX'),
    )
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=4, choices=FILE_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')  # FileField for file uploads

    def __str__(self):
        return self.file_name
     
     
     
class DownloadLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='download_links')
    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='download_links')
    encrypted_url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.encrypted_url
