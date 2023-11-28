from jet.dashboard.modules import DashboardModule
from django.contrib.auth.models import User

class NewUsers(DashboardModule):
    title = 'Usuarios por recibir'
    template = 'proposal_reception/dashboard_modules/recent_article_proposals.html'
    limit = 10

    def init_with_context(self, context):
        
            
        new_users = User.objects.filter(is_active=False)
        
        
         
        self.children.append({
                'title': 'Usuarios por recibir',
                'value' : new_users.count()
            })
            
            
