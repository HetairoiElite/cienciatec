from jet.dashboard.modules import DashboardModule
from apps.proposal_reception.models import ArticleProposal


class RecentArticleProposals(DashboardModule):
    title = 'Propuestas de artículo'
    template = 'proposal_reception/dashboard_modules/recent_article_proposals.html'
    limit = 10

    def init_with_context(self, context):
        por_recibir = ArticleProposal.objects.filter(status='1').count()
        por_asignar = ArticleProposal.objects.filter(status='2').count()
        en_revision = ArticleProposal.objects.filter(status='3').count()
        por_corregir = ArticleProposal.objects.filter(status='4').count()
        por_dictaminar = ArticleProposal.objects.filter(status='5').count()
        en_dictamen = ArticleProposal.objects.filter(status='6').count()
        from django.db.models import Q
        aceptados = ArticleProposal.objects.filter(
            Q(status='7') | Q(status='9') | Q(status='10')).distinct().count()
        rechazados = ArticleProposal.objects.filter(status='8').count()
        pendientes = ArticleProposal.objects.filter(status='9').count()
        por_publicar = ArticleProposal.objects.filter(status='10').count()

        self.children.append({
            'title': 'Por recibir',
            'value': f'{por_recibir} - {por_recibir * 100 / ArticleProposal.objects.count():.2f}%',
        })

        self.children.append({
            'title': 'Por asignar',
            'value': f'{por_asignar} - {por_asignar * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'En revisión',
            'value': f'{en_revision} - {en_revision * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            
            'title': 'Por corregir',
            'value': f'{por_corregir} - {por_corregir * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'Por dictaminar',
            'value': f'{por_dictaminar} - {por_dictaminar * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'En dictamen',
            'value': f'{en_dictamen} - {en_dictamen * 100 / ArticleProposal.objects.count():.2f}%',
        })
         
        self.children.append({
            'title': 'Aceptados',
            'value': f'{aceptados} - {aceptados * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'Rechazados',
            'value': f'{rechazados} - {rechazados * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'Pendientes',
            'value': f'{pendientes} - {pendientes * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({ 
            'title': 'Publicados',
            'value': f'{por_publicar} - {por_publicar * 100 / ArticleProposal.objects.count():.2f}%',
        })
        
        self.children.append({
            'title': 'Total',
            'value': f'{ArticleProposal.objects.count()}',
        })
        
         
