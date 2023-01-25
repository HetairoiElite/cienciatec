from django.db.models import manager


class PublicationManager(manager.Manager):
    def get_current(self):
        return self.get_queryset().filter(current=True).first()
# * get the current publication
