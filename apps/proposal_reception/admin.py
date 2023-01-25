from django.contrib import admin
from django.contrib import messages

from .models import *

# * user
from apps.registration.models import Profile

# * jet filters
from jet.filters import RelatedFieldAjaxListFilter

# Register your models here.


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    max_num = 5
    # readonly_fields = ('image',)
    show_change_link = True
    


class CoauthorInline(admin.TabularInline):
    model = Coauthor
    extra = 1
    
@admin.action(description='Enviar dictamen de arbitraje')
def send_arbitration_report(modeladmin, request, queryset):
    try:
        # * check if queryset has none approved articles
        
        if queryset.filter(is_approved=None).exists():
            raise Exception('Tiene artículos sin dictaminar')
        
        for article in queryset:
            article.send_arbitration_report()
            
                
        modeladmin.message_user(request, 'Se han enviado los dictámenes de arbitraje', level=messages.SUCCESS)
        
    except Exception as e:
        modeladmin.message_user(request, str(e), level=messages.ERROR)
    


class ArticleProposalAdmin(admin.ModelAdmin):
    
    actions = [send_arbitration_report]
    
    list_display = ('title', 'author', 'modality', 'template', 'is_approved')
    search_fields = ('title', 'author__user__username',
                     'author__user__first_name', 'author__user__last_name')

    inlines = [
        ArticleImageInline,
        CoauthorInline,
    ]
    
    # * jet filters
    list_filter = (
        ('author', RelatedFieldAjaxListFilter),
        ('school', RelatedFieldAjaxListFilter),
        ('modality'),
        ('is_approved')
    )



admin.site.register(ArticleProposal, ArticleProposalAdmin)
