
from django import forms

from .models import Assignment

from apps.registration.models import Profile

class AssignmentForm(forms.ModelForm):
    
    class Meta:
        model = Assignment
        fields = [
            'referee_assignment',
            'referees',
            'article',
        ]
        
        widgets = {
            'article': forms.Select(attrs={'class': 'form-control mb-2'}),
        }
        
        labels = {
            'referees': 'Arbitros',
            'article': 'Artículo',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("hola")
        # * concat queryset with option "Otra" with value "new"
        self.fields['referees'].choices = [('', '---------')] + \
            [(reviewer.id, reviewer.user.get_full_name())
             for reviewer in Profile.objects.filter(type_user="2")]
            
        print(self.fields['referees'].choices)
        # self.fields['article'].choices = [('', '---------')] + \
        #     [(article.id, article.title)
        #      for article in Article.objects.all()]