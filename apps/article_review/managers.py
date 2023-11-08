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

    def has_notes(self, assignment, user):
        notes = self.filter(assignment=assignment,
                            referee=user.profile)[0].notes.all().count()

        if notes > 0:
            return True
        else:
            return False

    def get_reported_reviews(self, assignment):
        # * count enviado = True reviews
        from django.db.models import Q
        return self.filter(Q(dictamen='1') | Q(dictamen='2'), assignment=assignment).count()

    def get_is_reported(self, assignment, user):
        # * check if review is sent
        try:
            review = self.filter(assignment=assignment, referee=user.profile)
            if review[0].dictamen == '1' or review[0].dictamen == '2':
                return True
            else:
                return False
        except:
            return False
