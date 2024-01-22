from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

 
class CustomUserModelAdmin(UserAdmin):
    

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "username",'tc',"otp", 'is_verified', 'is_active', 'is_admin', 'created_at', 'updated_at']

    list_filter = ['is_verified', 'is_active', 'is_admin']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'tc', 'password')}),
        ('Permissions', {'fields': ('is_verified', 'is_active', 'is_admin')}),
        ('Important dates', {'fields': ('last_login_time', 'last_logout_time', 'created_at', 'updated_at')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    #add_fieldsets needed when new user create in adminPanel
    add_fieldsets = (
        (
            None,
            {
                'classes': ['wide'],
                'fields': ('email', 'username', 'tc', 'password1', 'password2'),
            },
        ),
    )
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, CustomUserModelAdmin)