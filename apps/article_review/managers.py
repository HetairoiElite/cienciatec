from django.db.models import Manager


class ReviewManager(Manager):
    def get_sent_reviews(self, assignment):
        # * count enviado = True reviews
        return self.filter(enviado=True, assignment=assignment).count()

    def get_is_sent(self, assignment, user):
        # * check if review is sent
        try:
            review = self.filter(assignment=assignment, referee=user.profile)
            return review[0].enviado
        except:
            return False
