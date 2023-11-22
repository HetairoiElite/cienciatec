from django.db.models import manager

class AssignmentManager(manager.Manager):
    def get_assignments_by_pub(self, referee, publication):
        return self.filter(publication=publication, referees=referee)