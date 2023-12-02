from django.db.models import manager


class PublicationManager(manager.Manager):
    
    
    
    def get_current(self):
        try:
            return self.get_queryset().filter(current=True).first()
        except:
            pass
# * get the current publication
