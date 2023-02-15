from django.contrib import admin

# Register your models here.

from .models import *
from .forms import AssignmentForm

class AssignmentAdmin(admin.ModelAdmin):

    form = AssignmentForm
    
    readonly_fields = ('referee_assignment','article')
    

admin.site.register(Assignment, AssignmentAdmin)

admin.site.register(ArticleProfile)
admin.site.register(Profile)