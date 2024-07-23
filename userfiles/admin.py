from django.contrib import admin
from .models import User, File, DownloadLink
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "email", "name", "user_type", "is_admin", "created_at")
    list_filter = ('is_admin',)
    fieldsets = [
        ("User Credentials", {"fields": ["email","password"]}),
        ("Personal info", {"fields": ["name", "user_type"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "user_type","is_verified", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)


class FileAdmin(admin.ModelAdmin):
   list_display = ["id","file_name", "file_type", "uploaded_by", "uploaded_at"]

admin.site.register(File, FileAdmin)   



class DownloadLinkAdmin(admin.ModelAdmin):
   list_display = ["id", "file","client_user","encrypted_url","created_at","expires_at"]


admin.site.register(DownloadLink, DownloadLinkAdmin)