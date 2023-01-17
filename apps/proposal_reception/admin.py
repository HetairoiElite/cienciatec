from django.contrib import admin

from .models import *

# Register your models here.



class ProposalReceptionAdmin(admin.ModelAdmin):
    list_display = ['publication', 'start_date', 'end_date', 'notes']
    change_list_template = 'admin/events/change_list.html'


admin.site.register(ProposalReception, ProposalReceptionAdmin)