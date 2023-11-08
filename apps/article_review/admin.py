from django.contrib import admin

# Register your models here.

from .models import *

class NotesInline(admin.TabularInline):
    model = Note
    extra = 0
    fk_name = 'review'


class ArticleReviewAdmin(admin.ModelAdmin):

    inlines = [NotesInline]

    list_display = ('assignment',)
    
    readonly_fields = ('assignment',)


# admin.site.register(Review, ArticleReviewAdmin)
