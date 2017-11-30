import itertools
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.TextField(unique=True)
    parents = models.ManyToManyField('self', related_name='children', blank=True, symmetrical=False)

    def siblings(self):
        parents = self.parents.all()
        return [c for c in itertools.chain(*[p.children.all() for p in parents]) if c.id != self.id]
