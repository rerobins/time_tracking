from django.db import models
from django_extras.contrib.auth.models import SingleOwnerMixin
from django.contrib.auth.models import User


class Project(SingleOwnerMixin, models.Model):
    """
        Basic Project object that will group a selection of time records
        together.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    class Meta:
        unique_together = (('slug', 'owner'),)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail_view', (), {'project_slug': self.slug})

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
        Category that will allow for the type of work to be documented.
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)


class Location(SingleOwnerMixin, models.Model):
    """
        Location that can be applied to records to show that the time was spent
        in a specific location.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    location = models.CharField(max_length=255)


class Record(SingleOwnerMixin, models.Model):
    """
        Model object that will contain information about the start times of
        work on a project and the duration of the amount of time that the
        project was worked on.
    """
    project = models.ForeignKey(Project)
    brief_description = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)


