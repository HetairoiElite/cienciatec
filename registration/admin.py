from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_filter = ('username', 'email', 'first_name', 'last_name',
                   'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CustomProfileAdmin(admin.ModelAdmin):
    # model = Profile
    
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.avatar.url))
    
    image_tag.short_description = 'Avatar'
    
    list_display = ('user', 'image_tag', 'type_user' ,'school', 'created_at', 'updated_at')
    list_filter = ( 'type_user',)


admin.site.register(Profile, CustomProfileAdmin)
