from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models


# Register your models here.

class CustomProfileAdmin(admin.ModelAdmin):
    # model = Profile

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.avatar.url))

    image_tag.short_description = 'Avatar'

    list_display = ('user', 'image_tag', 'type_user',
                    'school', 'created_at', 'updated_at')
    list_filter = ('type_user',)


class InlineProfile(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('avatar', 'type_user', 'school', 'first_join')
    readonly_fields = ('first_join',)


class CustomUserAdmin(UserAdmin):
    
    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.profile.avatar.url))

    image_tag.short_description = 'Avatar'
    
    actions = None
    inlines = (InlineProfile,)
    model = User
    list_display = ('username', 'image_tag', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_filter = (
        'is_staff', 'is_active', 'is_superuser', 'date_joined', 'profile__type_user')
    fieldsets = (
        ('Cuenta', {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', )}),
        ('Permisos', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(Profile, CustomProfileAdmin)
