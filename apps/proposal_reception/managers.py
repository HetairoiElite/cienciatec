from django.db.models import QuerySet
from apps.reviewer_assignment.models import Assignment, ArticleProfile


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
            article_profile = ArticleProfile.objects.create(
                article=article_proposal,
                publication=article_proposal.publication,
            )
            # * save article profile
            article_profile.save()
            # * save assignment
            assignment.save()
            # * save article proposal
            article_proposal.save()

        return queryset
