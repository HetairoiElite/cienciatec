from django.contrib import admin
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
                    'school', 'created_at', 'updated_at')


class InlineProfile(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('avatar', 'type_user', 'school', 'first_join')

    readonly_fields = ('first_join',)

    radio_fields = {'type_user': admin.HORIZONTAL}


class CustomUserAdmin(UserAdmin):

    change_list_template = 'admin/users/change_list.html'

    def image_tag(self, obj):
        return format_html('<img src="{}" width="100" height="100" />'.format(obj.profile.avatar.url))

    image_tag.short_description = 'Avatar'

    def get_type_user(self, obj):
        return obj.profile.type_user

    get_type_user.short_description = 'Tipo de usuario'

    actions = None
    inlines = (InlineProfile,)
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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(Profile, CustomProfileAdmin)
