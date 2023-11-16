import uuid

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank, SearchVectorField
from django.db import models
from django.db.models import F

# Create your models here.

class WineQuerySet(models.query.QuerySet):
    def search(self, query):
        search_query = SearchQuery(query)
        return self.annotate(
            variety_headline=SearchHeadline(
                expression=F('variety'),
                highlight_all=True,
                query=search_query,
                start_sel='<mark>',
                stop_sel='</mark>',
            ),
            winery_headline=SearchHeadline(
                expression=F('winery'),
                highlight_all=True,
                query=search_query,
                start_sel='<mark>',
                stop_sel='</mark>',
            ),
            description_headline=SearchHeadline(
                expression=F('description'),
                highlight_all=True,
                query=search_query,
                start_sel='<mark>',
                stop_sel='</mark>',
            ),
            search_rank=SearchRank(F('search_vector'), search_query),
        ).filter(
            search_vector=search_query,
        ).order_by('-search_rank', 'id')

class Wine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    country = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    points = models.IntegerField()
    price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = WineQuerySet.as_manager()

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='search_vector_index')
        ]

    def __str__(self):
        return f'{self.id}'