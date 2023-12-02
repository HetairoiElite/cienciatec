from jet.dashboard.modules import DashboardModule
from apps.proposal_reception.models import ArticleProposal
from apps.publications.models import Publication


class RecentArticleProposals(DashboardModule):
    title = 'Propuestas de artículo'
    template = 'proposal_reception/dashboard_modules/recent_article_proposals.html'
    limit = 10

    def init_with_context(self, context):
        current_pub = Publication.objects.get_current()
        
        if current_pub:
            
            articles = ArticleProposal.objects.get_articles_by_pub(current_pub)
            
            por_recibir = articles.filter(status='1').count()
            por_asignar = articles.filter(status='2').count()
            en_revision = articles.filter(status='3').count()
            por_corregir = articles.filter(status='4').count()
            por_recibir_correcciones = articles.filter(status='5').count()
            por_dictaminar = articles.filter(status='6').count()
            en_dictamen = articles.filter(status='7').count()
            from django.db.models import Q
            aceptados = articles.filter(
                Q(status='8') | Q(status='10') | Q(status='11')).distinct().count()
            rechazados = articles.filter(status='9').count()
            pendientes = articles.filter(status='10').count()
            por_publicar = articles.filter(status='11').count()

            self.children.append(
                {
                    'title': 'Propuestas del periodo',
                    'value': '#' + str(current_pub.numero_publicacion)
                }
            )
            self.children.append({
                'title': 'Por recibir',
                'value': f'{por_recibir} - {por_recibir * 100 / articles.count():.2f}%',
            })

            self.children.append({
                'title': 'Por asignar',
                'value': f'{por_asignar} - {por_asignar * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'En revisión',
                'value': f'{en_revision} - {en_revision * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                
                'title': 'Por corregir',
                'value': f'{por_corregir} - {por_corregir * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                
                'title': 'Por recibir correcciones',
                'value': f'{por_recibir_correcciones} - {por_recibir_correcciones * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'Por dictaminar',
                'value': f'{por_dictaminar} - {por_dictaminar * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'En dictamen',
                'value': f'{en_dictamen} - {en_dictamen * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'Aceptados',
                'value': f'{aceptados} - {aceptados * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'Rechazados',
                'value': f'{rechazados} - {rechazados * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'Pendientes',
                'value': f'{pendientes} - {pendientes * 100 / articles.count():.2f}%',
            })
            
            self.children.append({ 
                'title': 'Publicados',
                'value': f'{por_publicar} - {por_publicar * 100 / articles.count():.2f}%',
            })
            
            self.children.append({
                'title': 'Total',
                'value': f'{articles.count()}',
            })
        else:
            self.children.append({
                'title': 'No hay periodo de publicación activo.',
                'value' :'Nada que mostrar'
            })
            
            
