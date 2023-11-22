from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from jet.filters import RelatedFieldAjaxListFilter
from django.contrib.admin import SimpleListFilter

# * import filters

# Register your models here.


class CustomProfileAdmin(admin.ModelAdmin):
    # model = Profile

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.avatar.url))

    image_tag.short_description = 'Avatar'

    list_display = ('user', 'image_tag', 'type_user',
                    'created_at', 'updated_at')


class InlineProfile(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    radio_fields = {'type_user': admin.HORIZONTAL}

    def get_fields(self, request, obj=None):
        if obj.profile.type_user != '2':
            return ('avatar', 'type_user', )
        else:
            return ('avatar', 'type_user', 'profiles')
        
    def get_readonly_fields(self, request, obj=None):
        if obj.profile.user.email:
            return ('type_user',)
        return ()


    # def get_readonly_fields(self, request, obj=None):
    #     if obj.profile.type_user != '2':
    #         return ('avatar',  )
    #     else:
    #         return ('avatar', 'profiles')

class CustomUserAdmin(UserAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.profile.avatar.url))

    image_tag.short_description = 'Avatar'

    def get_type_user(self, obj):
        try:

            return obj.profile.get_type_user_display()
        except:
            return None

    get_type_user.short_description = 'Tipo de usuario'

    inlines = (InlineProfile,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    
    model = User
    list_display = ('username', 'image_tag', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
                    'get_type_user')

    search_fields = ('username', 'email', 'first_name',
                     'last_name', 'profile__type_user')

    list_filter = (
        ('is_staff'),
        ('groups', RelatedFieldAjaxListFilter),
        ('is_active'),
        ('date_joined'),
        ('profile__type_user'),
    )

    # list_filter = (
    #     'is_staff', 'is_active', 'is_superuser', 'date_joined', 'profile__type_user')
    fieldsets = (
        ('Cuenta', {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', )}),
        ('Permisos', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('last_login', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(Profile, CustomProfileAdmin)
