from django.db import models
from django_extras.contrib.auth.models import SingleOwnerMixin

# Create your models here.


class Project(SingleOwnerMixin, models.Model):
    """
        Basic Project object that will group a selection of time records
        together.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)


class Record(SingleOwnerMixin, models.Model):
    """
        Model object that will contain information about the start times of
        work on a project and the duration of the amount of time that the
        project was worked on.
    """
    project = models.ForeignKey('Project')
    brief_description = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    categories = models.ManyToManyField('Category')
    location = models.ForeignKey('Location')


class Category(SingleOwnerMixin, models.Model):
    """
        Category that will allow for the type of work to be documented.
    """
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


