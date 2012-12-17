from django.db import models
from datetime import datetime

Q = models.Q
NOW = datetime.now()


class CollectionObjectManager(models.Manager):

    def published(self):
        return super(CollectionObjectManager, self).all().filter(
            Q(is_active=True),
            Q(from_date__lte=NOW),
            Q(to_date__gt=NOW) | Q(to_date__isnull=True),
        )

    def active(self):
        return super(CollectionObjectManager, self).all().filter(is_active=True)
