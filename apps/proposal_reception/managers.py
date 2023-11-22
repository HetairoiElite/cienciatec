from django.db.models import QuerySet
from apps.reviewer_assignment.models import Assignment


class ArticleProposalManager(QuerySet):

    # * update queryset
    def update_queryset(self, queryset):
        # * create assignment and article profile for each article proposal

        for article_proposal in queryset:
            # * create assignment
            assignment = Assignment.objects.create(
                article=article_proposal,
                publication=article_proposal.publication
            )
            # * create article profile
           
            # * save assignment
            assignment.save()
            # * save article proposal
            article_proposal.save()

        return queryset

    def get_articles_by_pub(self, publication):
        return self.filter(publication=publication)